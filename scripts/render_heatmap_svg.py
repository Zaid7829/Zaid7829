#!/usr/bin/env python3
"""
Render data/contributions.json as an animated unified terminal SVG heatmap.
Output: contrib-heatmap.svg (940x265)
"""
from __future__ import annotations
import json
import os
from pathlib import Path

DATA = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")
PALETTE = ["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353", "#69F0A0"]

W, H = 940, 265
X0, Y0 = 50, 56
CELL, GAP = 12, 4
STEP = CELL + GAP

def main():
    if not DATA.exists():
        raise SystemExit(f"Missing {DATA}")
        
    data = json.loads(DATA.read_text(encoding="utf-8"))
    days = data["days"]
    stats = data["stats"]
    static = os.getenv("STATIC") == "1"
    
    parts = [f'''  <!-- Terminal Container -->
  <rect width="{W}" height="{H}" rx="16" fill="#080B10"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="#30363D" stroke-width="1.2"/>
  
  <!-- Terminal Title Bar -->
  <rect x="1" y="1" width="{W-2}" height="40" rx="15" fill="#0D1117"/>
  <line x1="1" y1="41" x2="{W-1}" y2="41" stroke="#21262D" stroke-width="1"/>
  <circle cx="22" cy="21" r="5" fill="#FF5F56"/>
  <circle cx="38" cy="21" r="5" fill="#FFBD2E"/>
  <circle cx="54" cy="21" r="5" fill="#27C93F"/>
  <text x="76" y="25" fill="#8B949E" font-family="monospace" font-size="12">zaid@github:~$ git activity --year</text>
  <text x="{W-24}" y="25" text-anchor="end" fill="#39D353" font-family="monospace" font-size="11">CALENDAR: PUBLIC_LOGS</text>''']

    # Month Labels
    seen_months = set()
    for i, x in enumerate(days):
        d = x["date"]
        if d[8:10] <= "07" and d[:7] not in seen_months:
            seen_months.add(d[:7])
            col = i // 7
            parts.append(f'  <text x="{X0+col*STEP:.1f}" y="46" fill="#8B949E" font-family="monospace" font-size="10">{d[5:7]}/{d[2:4]}</text>')
            
    # Day of Week Labels
    for row, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        parts.append(f'  <text x="14" y="{Y0+row*STEP+10}" fill="#8B949E" font-family="monospace" font-size="9.5">{label}</text>')
        
    # Grid Cells
    for i, x in enumerate(days):
        col, row = i // 7, i % 7
        px = X0 + col * STEP
        py = Y0 + row * STEP
        lvl = max(0, min(5, int(x.get("level", 0))))
        
        if static:
            parts.append(f'  <rect x="{px}" y="{py}" width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[lvl]}"><title>{x["date"]}: {x["count"]} contribution(s)</title></rect>')
        else:
            delay = 0.15 + (col + row) * 0.018
            parts.append(f'''  <rect x="{px}" y="{py+4}" width="{CELL}" height="{CELL}" rx="3" fill="{PALETTE[lvl]}" opacity="0">
    <title>{x["date"]}: {x["count"]} contribution(s)</title>
    <animate attributeName="y" from="{py+4}" to="{py}" dur="0.35s" begin="{delay:.3f}s" fill="freeze"/>
    <animate attributeName="opacity" from="0" to="1" dur="0.30s" begin="{delay:.3f}s" fill="freeze"/>
  </rect>''')

    # Legend and Summary Footer
    ly = 188
    parts.append(f'  <text x="{X0}" y="{ly+24}" fill="#8B949E" font-family="monospace" font-size="10">Less</text>')
    for i, c in enumerate(PALETTE):
        parts.append(f'  <rect x="{X0+34+i*18}" y="{ly+14}" width="12" height="12" rx="3" fill="{c}"/>')
    parts.append(f'  <text x="{X0+34+6*18+6}" y="{ly+24}" fill="#8B949E" font-family="monospace" font-size="10">More</text>')
    
    parts.append(f'  <line x1="20" y1="{H-40}" x2="{W-20}" y2="{H-40}" stroke="#21262D" stroke-width="1"/>')
    parts.append(f'  <circle cx="28" cy="{H-20}" r="4" fill="#39D353"/>')
    parts.append(f'  <text x="40" y="{H-17}" fill="#C9D1D9" font-family="monospace" font-size="11">{stats["total"]:,} contributions (past year) • current streak {stats["current_streak"]}d • longest streak {stats["longest_streak"]}d</text>')
    parts.append(f'  <text x="{W-24}" y="{H-17}" text-anchor="end" fill="#8B949E" font-family="monospace" font-size="11">peak day: {stats["best_day"]["count"]} contributions</text>')

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated GitHub contribution heatmap for Zaid7829">
  <title>Zaid7829 — Contribution Heatmap</title>
  <desc>Public contribution calendar for Zaid7829 rendered with unified terminal design</desc>
{chr(10).join(parts)}
</svg>
'''
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT}")

if __name__ == "__main__":
    main()
