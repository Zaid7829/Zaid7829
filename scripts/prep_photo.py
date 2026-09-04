#!/usr/bin/env python3
"""Prepare a portrait for ASCII conversion."""
from __future__ import annotations
import sys
from pathlib import Path
import cv2
import numpy as np

OUT = Path("data/source-prepped.png")

def remove_background_with_rembg(image_path: Path):
    try:
        from rembg import remove
    except ImportError:
        return None
    from PIL import Image
    rgba = remove(Image.open(image_path).convert("RGBA"))
    arr = np.array(rgba)
    rgb, alpha = arr[:, :, :3], arr[:, :, 3]
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    return (gray * (alpha / 255.0) + 245 * (1 - alpha / 255.0)).astype(np.uint8)

def grabcut_fallback(bgr: np.ndarray) -> np.ndarray:
    h, w = bgr.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    rect = (int(w*0.18), int(h*0.10), int(w*0.64), int(h*0.88))
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, mask, rect, bgd, fgd, 8, cv2.GC_INIT_WITH_RECT)
    subject = np.where((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD), 1, 0).astype(np.uint8)
    subject = cv2.morphologyEx(subject, cv2.MORPH_CLOSE, np.ones((7,7), np.uint8), iterations=2)
    subject = cv2.morphologyEx(subject, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations=1)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return (gray * subject + 245 * (1-subject)).astype(np.uint8)

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/prep_photo.py path/to/photo.jpg")
    source = Path(sys.argv[1])
    if not source.exists():
        raise SystemExit(f"Photo not found: {source}")
    bgr = cv2.imread(str(source))
    if bgr is None:
        raise SystemExit(f"Could not read image: {source}")
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8,8))
    contrasted = clahe.apply(gray)
    rembg_result = remove_background_with_rembg(source)
    if rembg_result is not None:
        prepared = cv2.normalize(rembg_result, None, 0, 255, cv2.NORM_MINMAX)
        prepared = cv2.addWeighted(prepared, 0.72, contrasted, 0.28, 0)
    else:
        prepared = grabcut_fallback(bgr)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUT), prepared)
    print(f"Wrote {OUT}")

if __name__=="__main__":
    main()
