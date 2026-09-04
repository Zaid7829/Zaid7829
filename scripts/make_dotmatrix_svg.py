#!/usr/bin/env python3
"""
Generate and maintain avi-dotmatrix.svg (animated building portrait)
and avi-dotmatrix-static.svg (static portrait) matching the unified design system.
"""
from __future__ import annotations
import re
from pathlib import Path

PORTRAIT_ANIM = Path("avi-dotmatrix.svg")
PORTRAIT_STATIC = Path("avi-dotmatrix-static.svg")

BORDER_TAG = '<rect x="1" y="1" width="758" height="758" rx="17" fill="none" stroke="#30363D" stroke-width="1.2"/>\n'

T_CYCLE = 16.0
T_START = 0.4
T_BUILD = 7.0  # 7 seconds slow deliberate build
FADE_IN_TIME = 0.35
HOLD_END = 13.8
FADE_OUT_END = 15.0

def generate_animated_svg(base_content: str) -> str:
    # 1. Ensure border is present
    content = base_content
    if 'stroke="#30363D"' not in content and 'stroke="#30363d"' not in content:
        content = re.sub(
            r'(<rect width="760" height="760" rx="18"[^>]*/>\n?)',
            r'\1' + BORDER_TAG,
            content,
            count=1
        )

    # 2. Extract header up to the dot groups
    header_end = content.find('<g shape-rendering="geometricPrecision">')
    if header_end == -1:
        raise ValueError("Cannot locate dot groups in SVG")
    header = content[:header_end]

    # Remove any existing scanline rect or group
    header = re.sub(r'<rect x="34" y="0" width="692" height="2"[^>]*>.*?</rect>\s*', '', header, flags=re.DOTALL)
    header = re.sub(r'<g id="scanline">.*?</g>\s*', '', header, flags=re.DOTALL)

    # 3. Create synchronized amber scanline
    k_start = round(T_START / T_CYCLE, 5)
    k_build_end = round((T_START + T_BUILD) / T_CYCLE, 5)
    k_fade_line = round((T_START + T_BUILD + 0.4) / T_CYCLE, 5)
    k_hold = round(HOLD_END / T_CYCLE, 5)
    k_fade_out = round(FADE_OUT_END / T_CYCLE, 5)

    scanline_svg = f'''<g id="scanline">
  <rect x="34" y="50" width="692" height="3" fill="#ff9900" opacity="0">
    <animate attributeName="y" 
             values="50;50;750;750;750;50" 
             keyTimes="0;{k_start};{k_build_end};{k_hold};{k_fade_out};1" 
             dur="{T_CYCLE}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" 
             values="0;0.5;0.5;0;0;0" 
             keyTimes="0;{k_start};{k_build_end};{k_fade_line};{k_fade_out};1" 
             dur="{T_CYCLE}s" repeatCount="indefinite"/>
  </rect>
  <!-- Glow line -->
  <rect x="34" y="49" width="692" height="5" fill="#ff5500" opacity="0">
    <animate attributeName="y" 
             values="49;49;749;749;749;49" 
             keyTimes="0;{k_start};{k_build_end};{k_hold};{k_fade_out};1" 
             dur="{T_CYCLE}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" 
             values="0;0.25;0.25;0;0;0" 
             keyTimes="0;{k_start};{k_build_end};{k_fade_line};{k_fade_out};1" 
             dur="{T_CYCLE}s" repeatCount="indefinite"/>
  </rect>
</g>\n'''
    header = header + scanline_svg

    # 4. Extract all row groups
    groups_raw = re.findall(r'<g opacity="[^"]*">(.*?)</g>', content[header_end:], flags=re.DOTALL)
    num_rows = len(groups_raw)
    if num_rows == 0:
        raise ValueError("Zero dot groups extracted")

    new_groups = []
    for i, g_body in enumerate(groups_raw):
        clean_body = re.sub(r'<animate[^>]*/>\s*', '', g_body).strip()
        t1 = T_START + (i / max(1, num_rows - 1)) * T_BUILD
        t2 = t1 + FADE_IN_TIME

        k0 = 0.0
        k1 = round(t1 / T_CYCLE, 5)
        k2 = round(t2 / T_CYCLE, 5)
        k3 = round(HOLD_END / T_CYCLE, 5)
        k4 = round(FADE_OUT_END / T_CYCLE, 5)
        k5 = 1.0

        if k2 <= k1:
            k2 = round(k1 + 0.001, 5)
        if k3 <= k2:
            k3 = round(k2 + 0.001, 5)

        kt_str = f"{k0};{k1};{k2};{k3};{k4};{k5}"
        val_str = "0;0;1;1;0;0"

        anim_tag = f'<animate attributeName="opacity" values="{val_str}" keyTimes="{kt_str}" dur="{T_CYCLE}s" repeatCount="indefinite"/>'
        new_groups.append(f'<g opacity="0">{clean_body}{anim_tag}</g>')

    # 5. Assemble footer
    footer = '''</g>
<g font-family="monospace" font-size="12" fill="#8b949e" opacity=".72">
<text x="34" y="728">zaid@github:~$ ./render --portrait</text>
<text x="34" y="747" fill="#ffad33">●</text><text x="48" y="747">dotmatrix.svg</text>
</g>
</svg>'''

    return header + '<g shape-rendering="geometricPrecision">' + "".join(new_groups) + footer

def generate_static_svg(anim_content: str) -> str:
    # 1. Remove scanline group
    static_svg = re.sub(r'<g id="scanline">.*?</g>\s*', '', anim_content, flags=re.DOTALL)
    # 2. Remove any leftover animate tags
    static_svg = re.sub(r'<animate[^>]*/>\s*', '', static_svg)
    # 3. Ensure all dot groups have opacity="1"
    static_svg = re.sub(r'<g opacity="0">', '<g opacity="1">', static_svg)
    # 4. Update title
    static_svg = re.sub(
        r'<title>.*?</title>',
        '<title>Zaid7829 — static dot-matrix portrait</title>',
        static_svg,
        count=1
    )
    return static_svg

def main():
    if not PORTRAIT_ANIM.exists():
        raise SystemExit(f"Missing {PORTRAIT_ANIM}")

    base_content = PORTRAIT_ANIM.read_text(encoding="utf-8")
    anim_svg = generate_animated_svg(base_content)
    PORTRAIT_ANIM.write_text(anim_svg, encoding="utf-8")
    print(f"Generated {PORTRAIT_ANIM} ({len(anim_svg.encode('utf-8')) / 1024:.1f} KB)")

    static_svg = generate_static_svg(anim_svg)
    PORTRAIT_STATIC.write_text(static_svg, encoding="utf-8")
    print(f"Generated {PORTRAIT_STATIC} ({len(static_svg.encode('utf-8')) / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
