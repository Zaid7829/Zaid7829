#!/usr/bin/env python3
"""
Ensure avi-dotmatrix.svg and avi-dotmatrix-static.svg match the unified design system.
Maintains the high-density dot matrix portrait while enforcing the global border and geometry.
"""
from __future__ import annotations
import re
from pathlib import Path

PORTRAIT_ANIM = Path("avi-dotmatrix.svg")
PORTRAIT_STATIC = Path("avi-dotmatrix-static.svg")

BORDER_TAG = '<rect x="1" y="1" width="758" height="758" rx="17" fill="none" stroke="#30363D" stroke-width="1.2"/>\n'

def main():
    if not PORTRAIT_ANIM.exists():
        raise SystemExit(f"Missing {PORTRAIT_ANIM}")
        
    content = PORTRAIT_ANIM.read_text(encoding="utf-8")
    
    # 1. Ensure border is present in animated SVG
    if 'stroke="#30363D"' not in content and 'stroke="#30363d"' not in content:
        # Insert right after the background rect
        content = re.sub(
            r'(<rect width="760" height="760" rx="18"[^>]*/>\n?)',
            r'\1' + BORDER_TAG,
            content,
            count=1
        )
        PORTRAIT_ANIM.write_text(content, encoding="utf-8")
        print(f"Updated border in {PORTRAIT_ANIM}")
    else:
        print(f"Border already verified in {PORTRAIT_ANIM}")
        
    # 2. Generate static version
    # Remove animate tags
    static_svg = re.sub(r'<animate[^>]*/>\s*', '', content)
    # Remove scanline rect
    static_svg = re.sub(r'<rect x="34" y="0" width="692" height="2"[^>]*>.*?</rect>\s*', '', static_svg, flags=re.DOTALL)
    # Ensure all groups have opacity="1"
    static_svg = re.sub(r'opacity="0"', 'opacity="1"', static_svg)
    
    # Update title
    static_svg = re.sub(
        r'<title>.*?</title>',
        '<title>Zaid7829 — static dot-matrix portrait</title>',
        static_svg,
        count=1
    )
    
    PORTRAIT_STATIC.write_text(static_svg, encoding="utf-8")
    print(f"Generated {PORTRAIT_STATIC} ({len(static_svg.encode('utf-8')) / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
