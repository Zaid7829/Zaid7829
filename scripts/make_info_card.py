#!/usr/bin/env python3
"""
Generate the unified terminal developer system information card for Zaid7829.
Output: info-card.svg (760x760)
"""
from __future__ import annotations
import html
import json
import os
from pathlib import Path

PROFILE_PATH = Path("data/profile.json")
OUTPUT_PATH = Path("info-card.svg")

W, H = 760, 760

def esc(text: str) -> str:
    return html.escape(str(text), quote=True)

def join_items(items: list[str], max_items: int = 5) -> str:
    return " · ".join(items[:max_items])

def main():
    if not PROFILE_PATH.exists():
        raise SystemExit(f"Missing {PROFILE_PATH}")
        
    p = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    static = os.getenv("STATIC") == "1"
    
    # Structured key-value rows
    rows = [
        ("USER", p.get("username", "Zaid7829"), "#E6EDF3"),
        ("ROLE", p.get("role", "Full Stack Developer"), "#FF8C00"),
        ("FOCUS", "Full-Stack Web · API Design · Architecture", "#E6EDF3"),
        ("LANGS", join_items(p.get("languages", []), 6), "#C9D1D9"),
        ("FRONTEND", join_items(p.get("frontend", []), 5), "#C9D1D9"),
        ("BACKEND", join_items(p.get("backend", []), 5), "#C9D1D9"),
        ("APIS", join_items(p.get("apis", []), 4), "#C9D1D9"),
        ("DATABASE", join_items(p.get("data", []), 5), "#C9D1D9"),
        ("CLOUD/OPS", join_items(p.get("cloud", []), 5), "#C9D1D9"),
        ("TESTING", join_items(p.get("testing", []), 5), "#C9D1D9"),
        ("AI / ML", join_items(p.get("ai", []), 4), "#C9D1D9"),
        ("KERNEL", p.get("system", "x86_64 Full Stack Dev OS // kernel 6.x"), "#8B949E"),
        ("STATUS", p.get("currently", "BUILDING · LEARNING · SHIPPING"), "#39D353"),
    ]
    
    parts = []
    
    # Container & Gradients
    parts.append(f'''  <defs>
    <radialGradient id="card-bg" cx="50%" cy="40%" r="75%">
      <stop offset="0%" stop-color="#11151c"/>
      <stop offset="55%" stop-color="#0a0d12"/>
      <stop offset="100%" stop-color="#050608"/>
    </radialGradient>
  </defs>
  
  <!-- Terminal Outer Frame -->
  <rect width="{W}" height="{H}" rx="18" fill="url(#card-bg)"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="none" stroke="#30363D" stroke-width="1.2"/>
  
  <!-- Top Terminal Bar -->
  <rect x="1" y="1" width="{W-2}" height="42" rx="17" fill="#0D1117"/>
  <line x1="1" y1="43" x2="{W-1}" y2="43" stroke="#21262D" stroke-width="1"/>
  <circle cx="24" cy="22" r="5" fill="#FF5F56"/>
  <circle cx="40" cy="22" r="5" fill="#FFBD2E"/>
  <circle cx="56" cy="22" r="5" fill="#27C93F"/>
  <text x="78" y="26" fill="#8B949E" font-family="monospace" font-size="12">zaid@github:~$ ./system --profile --specs</text>
  <text x="{W-26}" y="26" text-anchor="end" fill="#39D353" font-family="monospace" font-size="11">● ONLINE [DEV-OS]</text>
  
  <!-- Terminal Content Header -->
  <text x="36" y="80" fill="#FF8C00" font-family="monospace" font-size="22" font-weight="700">{esc(p.get("username", "ZAID7829").upper())}</text>
  <text x="36" y="104" fill="#8B949E" font-family="monospace" font-size="12">{esc(p.get("tagline", "Building complete software from interface to deployment."))}</text>
  <line x1="36" y1="122" x2="{W-36}" y2="122" stroke="#21262D" stroke-width="1"/>''')

    # Rows layout
    start_y = 158
    row_gap = 39
    for i, (k, v, val_color) in enumerate(rows):
        y = start_y + i * row_gap
        delay = 0.15 + i * 0.07
        
        # Row content
        label_svg = f'<text x="36" y="{y}" fill="#FF8C00" font-family="monospace" font-size="11" font-weight="700">{esc(k.ljust(9))}</text>'
        div_svg = f'<text x="122" y="{y}" fill="#30363D" font-family="monospace" font-size="11">│</text>'
        val_svg = f'<text x="140" y="{y}" fill="{val_color}" font-family="monospace" font-size="11">{esc(v)}</text>'
        
        if static:
            parts.append(f'  <g>{label_svg}{div_svg}{val_svg}</g>')
        else:
            parts.append(f'''  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="-6 0" to="0 0" dur="0.4s" begin="{delay:.2f}s" fill="freeze"/>
    {label_svg}
    {div_svg}
    {val_svg}
  </g>''')

    # Card footer
    footer_y = H - 52
    parts.append(f'''  <!-- Terminal Footer Specs -->
  <line x1="36" y1="{footer_y}" x2="{W-36}" y2="{footer_y}" stroke="#21262D" stroke-width="1"/>
  <circle cx="44" cy="{footer_y+26}" r="4" fill="#FF8C00"/>
  <text x="56" y="{footer_y+29}" fill="#8B949E" font-family="monospace" font-size="11">PHILOSOPHY: Clean Architecture · Performance · Security · DX</text>
  <text x="{W-36}" y="{footer_y+29}" text-anchor="end" fill="#6E7681" font-family="monospace" font-size="11">UPTIME: CONTINUOUS // 2026</text>''')

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal developer information card for Zaid7829">
  <title>Zaid7829 — Developer System Card</title>
  <desc>Neofetch developer information card detailing full stack role, skills, and status</desc>
{chr(10).join(parts)}
</svg>
'''
    OUTPUT_PATH.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
