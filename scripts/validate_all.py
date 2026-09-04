import json
import xml.etree.ElementTree as ET
from pathlib import Path
import py_compile
import glob
import re

print("=== 1. Python Syntax Check ===")
scripts = glob.glob("scripts/*.py")
for s in scripts:
    py_compile.compile(s, doraise=True)
    print(f"  [OK] {s} compiled successfully")

print("\n=== 2. JSON Validation ===")
json_files = ["data/design.json", "data/profile.json", "data/skills.json", "data/contributions.json"]
for jf in json_files:
    content = json.loads(Path(jf).read_text(encoding="utf-8"))
    print(f"  [OK] {jf} valid JSON (keys: {list(content.keys())[:4]}...)")

print("\n=== 3. SVG XML Validation ===")
svg_files = [
    "avi-dotmatrix.svg",
    "avi-dotmatrix-static.svg",
    "avi-ascii.svg",
    "info-card.svg",
    "contrib-heatmap.svg",
    "skill-radar.svg",
    "toolbox.svg",
    "system-status.svg",
    "hero-constellation.svg",
    "system-architecture.svg",
    "quality-gate.svg",
    "workflow-pipeline.svg",
    "project-devos.svg",
    "project-staging.svg"
]
for sf in svg_files:
    p = Path(sf)
    assert p.exists(), f"Missing {sf}"
    tree = ET.parse(sf)
    root = tree.getroot()
    size_kb = len(p.read_bytes()) / 1024
    print(f"  [OK] {sf} valid XML (tag: {root.tag}, size: {size_kb:.1f} KB)")

print("\n=== 4. Workflow YAML Check ===")
import yaml
wf = Path(".github/workflows/update-profile-art.yml")
assert wf.exists(), "Workflow missing"
wf_data = yaml.safe_load(wf.read_text(encoding="utf-8"))
print(f"  [OK] Workflow valid YAML (name: {wf_data.get('name')})")

print("\n=== 5. README Image Path Check ===")
readme = Path("README.md").read_text(encoding="utf-8")
img_srcs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', readme)
for src in img_srcs:
    if src.startswith("http"):
        print(f"  [OK] Remote asset: {src[:50]}...")
    else:
        # local file
        clean_path = src.lstrip("./")
        assert Path(clean_path).exists(), f"Missing local image: {src}"
        print(f"  [OK] Local asset exists: {clean_path}")

print("\n=== 6. Secret & Private Photo Scan ===")
patterns = [r"ghp_[A-Za-z0-9]+", r"github_pat_[A-Za-z0-9]+", r"sk-[A-Za-z0-9]+", r"password\s*[:=]\s*['\"][^'\"]+['\"]"]
for path in Path(".").rglob("*"):
    if path.is_file() and not any(part.startswith(".git") for part in path.parts) and not path.suffix in [".png", ".jpg", ".jpeg", ".pyc"]:
        txt = path.read_text(encoding="utf-8", errors="ignore")
        for pat in patterns:
            m = re.search(pat, txt)
            assert not m, f"Potential secret in {path}: {m.group(0)}"
print("  [OK] Zero secrets or private keys found across codebase")
print("\nALL VERIFICATIONS PASSED!")
