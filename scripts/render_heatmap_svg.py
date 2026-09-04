#!/usr/bin/env python3
"""
Render data/contributions.json as an animated unified terminal SVG heatmap.
Features subtle, organic, randomized activity animations across contribution cells
resembling living developer activity throughout the year.
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

# 18 organic wandering single-cell pulses
# (col, row, class_name, dur, delay, target_lvl)
# Durations are non-harmonic primes / co-primes between 18s and 34s
# Delays are well-distributed (0.8s to 11.2s) so 1-3 cells are active at a time
SINGLE_CELLS = [
    (3, 1, "p-01", 19.3, 0.8, 3),
    (6, 4, "p-02", 23.1, 4.2, 4),
    (9, 2, "p-03", 27.4, 8.1, 2),
    (12, 5, "p-04", 21.7, 2.5, 4),
    (16, 1, "p-05", 29.3, 9.4, 5),
    (19, 6, "p-06", 24.2, 5.7, 3),
    (22, 3, "p-07", 31.1, 1.4, 2),
    (25, 0, "p-08", 22.8, 6.9, 4),
    (27, 5, "p-09", 26.6, 3.1, 3),
    (31, 2, "p-10", 33.5, 10.5, 5),
    (34, 4, "p-11", 20.2, 1.9, 3),
    (37, 1, "p-12", 28.8, 7.3, 4),
    (40, 6, "p-13", 23.9, 3.8, 2),
    (42, 3, "p-14", 30.4, 8.6, 4),
    (45, 5, "p-15", 25.1, 4.9, 3),
    (47, 0, "p-16", 32.7, 11.2, 4),
    (49, 4, "p-17", 21.3, 2.1, 5),
    (51, 2, "p-18", 27.9, 6.3, 2),
]

# 3 occasional small clusters (2-4 nearby cells activating together with micro-delays)
CLUSTER_CELLS = [
    # Cluster A (Spring sprint, week 14-15, 3 cells nearby)
    (14, 2, "cl-a1", 38.0, 5.0, 3),
    (14, 3, "cl-a2", 38.0, 5.3, 4),
    (15, 2, "cl-a3", 38.0, 5.6, 3),
    # Cluster B (Summer feature burst, week 28-29, 4 cells nearby)
    (28, 3, "cl-b1", 44.0, 14.0, 2),
    (28, 4, "cl-b2", 44.0, 14.3, 4),
    (29, 3, "cl-b3", 44.0, 14.6, 5),
    (29, 4, "cl-b4", 44.0, 14.9, 3),
    # Cluster C (Winter release push, week 43-44, 3 cells nearby)
    (43, 1, "cl-c1", 49.0, 22.0, 3),
    (43, 2, "cl-c2", 49.0, 22.35, 4),
    (44, 2, "cl-c3", 49.0, 22.7, 4),
]

def main():
    if not DATA.exists():
        raise SystemExit(f"Missing {DATA}")

    data = json.loads(DATA.read_text(encoding="utf-8"))
    days = data["days"]
    stats = data["stats"]
    static = os.getenv("STATIC") == "1"

    all_anims = SINGLE_CELLS + CLUSTER_CELLS
    anim_map = {}
    if not static:
        for col, row, cname, dur, delay, tgt_lvl in all_anims:
            idx = col * 7 + row
            if idx < len(days):
                anim_map[idx] = (cname, dur, delay, tgt_lvl)

    parts = []

    # Inject CSS animation styles into <defs> if animated
    if not static:
        style_lines = [
            '  <defs>',
            '    <style>',
            '      /* Living GitHub Contribution Heatmap - Organic Activity Animations */',
            '      @keyframes pulseLvl2 {',
            '        0% { fill: #161B22; }',
            '        2% { fill: #006D32; }',
            '        8% { fill: #006D32; }',
            '        13% { fill: #161B22; }',
            '        100% { fill: #161B22; }',
            '      }',
            '      @keyframes pulseLvl3 {',
            '        0% { fill: #161B22; }',
            '        2% { fill: #26A641; }',
            '        8% { fill: #26A641; }',
            '        13% { fill: #161B22; }',
            '        100% { fill: #161B22; }',
            '      }',
            '      @keyframes pulseLvl4 {',
            '        0% { fill: #161B22; }',
            '        2% { fill: #39D353; }',
            '        8% { fill: #39D353; }',
            '        13% { fill: #161B22; }',
            '        100% { fill: #161B22; }',
            '      }',
            '      @keyframes pulseLvl5 {',
            '        0% { fill: #161B22; }',
            '        2% { fill: #69F0A0; }',
            '        8% { fill: #69F0A0; }',
            '        13% { fill: #161B22; }',
            '        100% { fill: #161B22; }',
            '      }',
        ]
        for _, _, cname, dur, delay, tgt_lvl in all_anims:
            kf = f"pulseLvl{tgt_lvl}"
            style_lines.append(f'      .{cname} {{ animation: {kf} {dur:.1f}s {delay:.2f}s cubic-bezier(0.4, 0, 0.2, 1) infinite; }}')
        style_lines.extend([
            '      /* Respect user motion preferences */',
            '      @media (prefers-reduced-motion: reduce) {',
            '        .live-cell { animation: none !important; }',
            '      }',
            '    </style>',
            '  </defs>',
        ])
        parts.append("\n".join(style_lines))

    # Terminal Container
    parts.append(f'''  <!-- Terminal Container -->
  <rect width="{W}" height="{H}" rx="16" fill="#080B10"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="#30363D" stroke-width="1.2"/>
  
  <!-- Terminal Title Bar -->
  <rect x="1" y="1" width="{W-2}" height="40" rx="15" fill="#0D1117"/>
  <line x1="1" y1="41" x2="{W-1}" y2="41" stroke="#21262D" stroke-width="1"/>
  <circle cx="22" cy="21" r="5" fill="#FF5F56"/>
  <circle cx="38" cy="21" r="5" fill="#FFBD2E"/>
  <circle cx="54" cy="21" r="5" fill="#27C93F"/>
  <text x="76" y="25" fill="#8B949E" font-family="monospace" font-size="12">zaid@github:~$ git activity --year</text>
  <text x="{W-24}" y="25" text-anchor="end" fill="#39D353" font-family="monospace" font-size="11">CALENDAR: PUBLIC_LOGS</text>''')

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
        base_color = PALETTE[lvl]

        if not static and i in anim_map:
            cname = anim_map[i][0]
            parts.append(f'  <rect class="live-cell {cname}" x="{px}" y="{py}" width="{CELL}" height="{CELL}" rx="3" fill="{base_color}"><title>{x["date"]}: {x["count"]} contribution(s)</title></rect>')
        else:
            parts.append(f'  <rect x="{px}" y="{py}" width="{CELL}" height="{CELL}" rx="3" fill="{base_color}"><title>{x["date"]}: {x["count"]} contribution(s)</title></rect>')

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
    print(f"Wrote {OUTPUT} ({len(svg.encode('utf-8'))/1024:.1f} KB)")

if __name__ == "__main__":
    main()
