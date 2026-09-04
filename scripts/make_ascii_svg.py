#!/usr/bin/env python3
"""Convert data/source-prepped.png into an animated ASCII SVG."""
from __future__ import annotations
import html
import os
from pathlib import Path
import cv2
import numpy as np

SOURCE = Path("data/source-prepped.png")
OUTPUT = Path("avi-ascii.svg")
RAMP = " .`:-=+*cs#%@"
COLS, ROWS = 96, 52
SVG_W, SVG_H = 760, 560
CHAR_W, LINE_H = 7.55, 9.25

def glyph(value: int) -> str:
    idx = int((255-int(value))*(len(RAMP)-1)/255)
    return RAMP[max(0, min(len(RAMP)-1, idx))]

def build_rows():
    image = cv2.imread(str(SOURCE), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise SystemExit(f"Missing {SOURCE}. Run prep_photo.py first.")
    h, w = image.shape
    crop = image[int(h*0.08):int(h*0.99), int(w*0.20):int(w*0.85)]
    small = cv2.resize(crop, (COLS, ROWS), interpolation=cv2.INTER_AREA)
    small = np.clip((small.astype(np.float32)-118)*1.25+128, 0, 255).astype(np.uint8)
    rows = ["".join(glyph(v) for v in row).rstrip() for row in small]
    active = np.array([[c!=" " for c in row.ljust(COLS)] for row in rows])
    cols = np.where(active.any(axis=0))[0]
    if len(cols):
        rows = [row.ljust(COLS)[cols[0]:cols[-1]+1] for row in rows]
    return rows

def esc(text): return html.escape(text, quote=True)

def main():
    rows = build_rows()
    cols = max(map(len, rows))
    art_w = cols*CHAR_W
    art_x = (SVG_W-art_w)/2
    art_y = 55
    static = os.getenv("STATIC")=="1"
    parts = [f'''<rect width="{SVG_W}" height="{SVG_H}" rx="18" fill="#0d1117"/>
<rect x="1" y="1" width="{SVG_W-2}" height="{SVG_H-2}" rx="17" fill="none" stroke="#30363d"/>
<circle cx="24" cy="22" r="5" fill="#ff7b72"/><circle cx="42" cy="22" r="5" fill="#d29922"/><circle cx="60" cy="22" r="5" fill="#3fb950"/>
<text x="78" y="26" fill="#8b949e" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12">zaid@github:~$ ./portrait --render</text>''']
    for i, row in enumerate(rows):
        y=art_y+i*LINE_H
        if static:
            parts.append(f'''<text x="{art_x:.1f}" y="{y:.1f}" xml:space="preserve" fill="#c9d1d9" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="8.7" font-weight="600">{esc(row)}</text>''')
        else:
            delay=0.10+i*0.055
            cid=f"wipe{i}"
            parts.append(f'''<clipPath id="{cid}"><rect x="{art_x:.1f}" y="{y-LINE_H+1:.1f}" width="0" height="{LINE_H+2:.1f}">
<animate attributeName="width" from="0" to="{art_w:.1f}" dur="0.75s" begin="{delay:.2f}s" fill="freeze"/>
</rect></clipPath>
<text x="{art_x:.1f}" y="{y:.1f}" xml:space="preserve" clip-path="url(#{cid})" fill="#c9d1d9" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="8.7" font-weight="600">{esc(row)}</text>
<rect x="{art_x:.1f}" y="{y-LINE_H+1:.1f}" width="4" height="{LINE_H+2:.1f}" rx="1" fill="#58a6ff" opacity="0.85">
<animate attributeName="x" from="{art_x:.1f}" to="{art_x+art_w:.1f}" dur="0.75s" begin="{delay:.2f}s" fill="freeze"/>
<animate attributeName="opacity" from="0.85" to="0" dur="0.15s" begin="{delay+0.75:.2f}s" fill="freeze"/>
</rect>''')
    parts.append(f'''<text x="{SVG_W/2}" y="{SVG_H-14}" text-anchor="middle" fill="#8b949e" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11">FULL STACK DEVELOPER • BUILDING FROM FRONTEND TO BACKEND</text>''')
    svg=f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}" role="img" aria-label="Animated monochrome ASCII portrait of Zaid7829">
<title>Zaid7829 animated ASCII portrait</title>
{chr(10).join(parts)}
</svg>
'''
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT}")

if __name__=="__main__": main()
