#!/usr/bin/env python3
"""
Render data/contributions.json as an animated unified terminal SVG heatmap.
Features:
- 30+ glowing contribution cells with organic randomized activity animations
- Playful animated snake roaming across the contribution grid cells
- Full preservation of authentic contribution counts and stats
- Reduced-motion accessibility support
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

# 32 organic wandering single-cell pulses (30+ cells requirement)
# (col, row, class_name, dur, delay, target_lvl)
# Durations are non-harmonic primes / co-primes between 15s and 33s
# Delays are distributed between 0.5s and 10.5s
SINGLE_CELLS = [
    (1, 2, "p-01", 16.3, 0.5, 3),
    (3, 5, "p-02", 21.1, 3.2, 4),
    (5, 1, "p-03", 18.4, 1.8, 2),
    (7, 4, "p-04", 24.7, 5.1, 4),
    (9, 0, "p-05", 19.3, 0.9, 5),
    (11, 6, "p-06", 27.1, 4.4, 3),
    (13, 3, "p-07", 15.8, 2.1, 2),
    (16, 2, "p-08", 22.9, 6.7, 4),
    (18, 5, "p-09", 17.6, 1.2, 3),
    (19, 1, "p-10", 25.4, 8.3, 5),
    (22, 4, "p-11", 20.7, 2.8, 3),
    (24, 0, "p-12", 28.3, 5.9, 4),
    (26, 6, "p-13", 16.9, 0.7, 2),
    (27, 2, "p-14", 23.5, 3.9, 4),
    (30, 5, "p-15", 19.8, 7.1, 3),
    (32, 1, "p-16", 26.2, 1.6, 5),
    (34, 4, "p-17", 18.9, 4.8, 2),
    (36, 0, "p-18", 24.1, 9.2, 4),
    (37, 6, "p-19", 21.5, 2.4, 3),
    (39, 3, "p-20", 17.2, 5.6, 4),
    (41, 1, "p-21", 29.7, 0.8, 3),
    (42, 5, "p-22", 22.1, 3.5, 5),
    (44, 4, "p-23", 15.4, 6.2, 2),
    (46, 0, "p-24", 27.8, 1.4, 4),
    (47, 6, "p-25", 20.3, 4.1, 3),
    (48, 2, "p-26", 23.9, 8.7, 4),
    (49, 5, "p-27", 18.1, 2.6, 2),
    (50, 1, "p-28", 26.5, 5.3, 5),
    (51, 4, "p-29", 16.7, 1.1, 3),
    (52, 0, "p-30", 22.4, 7.8, 4),
    (52, 6, "p-31", 28.9, 3.7, 3),
    (14, 0, "p-32", 19.5, 6.0, 4),
]

# 4 occasional small clusters (2-4 nearby cells activating together with micro-delays)
CLUSTER_CELLS = [
    # Cluster A (Autumn sprint, week 8-9, 3 cells)
    (8, 2, "cl-a1", 32.0, 4.0, 3),
    (8, 3, "cl-a2", 32.0, 4.25, 4),
    (9, 3, "cl-a3", 32.0, 4.55, 3),
    # Cluster B (Spring burst, week 20-21, 3 cells)
    (20, 2, "cl-b1", 37.0, 11.0, 2),
    (20, 3, "cl-b2", 37.0, 11.3, 4),
    (21, 3, "cl-b3", 37.0, 11.6, 5),
    # Cluster C (Summer feature push, week 33-34, 4 cells)
    (33, 2, "cl-c1", 41.0, 18.0, 3),
    (33, 3, "cl-c2", 41.0, 18.25, 4),
    (34, 2, "cl-c3", 41.0, 18.55, 5),
    (34, 3, "cl-c4", 41.0, 18.85, 3),
    # Cluster D (Winter release, week 44-45, 3 cells)
    (44, 2, "cl-d1", 45.0, 25.0, 3),
    (44, 3, "cl-d2", 45.0, 25.35, 4),
    (45, 3, "cl-d3", 45.0, 25.7, 4),
]

def generate_snake_path() -> tuple[str, float]:
    """Generate a Manhattan grid-aligned closed wandering path for the snake."""
    waypoints = [
        (4, 2), (8, 2), (8, 5), (13, 5), (13, 1), (17, 1), (17, 4),
        (21, 4), (21, 0), (26, 0), (26, 3), (30, 3), (30, 6), (35, 6),
        (35, 2), (39, 2), (39, 5), (44, 5), (44, 1), (48, 1), (48, 4),
        (51, 4), (51, 6), (42, 6), (42, 0), (33, 0), (33, 4), (24, 4),
        (24, 6), (15, 6), (15, 3), (4, 3), (4, 2)
    ]
    grid_points = [waypoints[0]]
    for target in waypoints[1:]:
        cur = grid_points[-1]
        c, r = cur
        tc, tr = target
        step_c = 1 if tc > c else -1
        while c != tc:
            c += step_c
            grid_points.append((c, r))
        step_r = 1 if tr > r else -1
        while r != tr:
            r += step_r
            grid_points.append((c, r))

    coords = [(56 + c * 16, 62 + r * 16) for c, r in grid_points]
    d_parts = [f"M {coords[0][0]},{coords[0][1]}"]
    for x, y in coords[1:]:
        d_parts.append(f"L {x},{y}")
    d_parts.append("Z")
    
    total_steps = len(grid_points)
    # Each step takes ~0.20s -> total loop ~29.4s
    dur = round(total_steps * 0.20, 1)
    return " ".join(d_parts), dur, 0.20

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
            '      /* Living GitHub Contribution Heatmap - 30+ Glowing Activity Cells */',
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
            '        #snake-entity { display: none !important; }',
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

    # Grid Cells (371 cells with 30+ glowing live-cells)
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

    # Animated Roaming Snake Entity
    if not static:
        snake_path_d, snake_dur, step_dur = generate_snake_path()
        dt1 = f"-{step_dur * 1:.2f}s"
        dt2 = f"-{step_dur * 2:.2f}s"
        dt3 = f"-{step_dur * 3:.2f}s"
        dt4 = f"-{step_dur * 4:.2f}s"

        parts.append(f'''  <!-- Animated Roaming Snake -->
  <g id="snake-entity">
    <!-- Tail (trailing segment) -->
    <rect x="-5" y="-5" width="10" height="10" rx="2.5" fill="#0E4429" opacity="0.85">
      <animateMotion dur="{snake_dur}s" repeatCount="indefinite" begin="{dt4}" path="{snake_path_d}" />
    </rect>
    <!-- Body Segment 3 -->
    <rect x="-6" y="-6" width="12" height="12" rx="3" fill="#006D32" opacity="0.9">
      <animateMotion dur="{snake_dur}s" repeatCount="indefinite" begin="{dt3}" path="{snake_path_d}" />
    </rect>
    <!-- Body Segment 2 -->
    <rect x="-6" y="-6" width="12" height="12" rx="3" fill="#26A641">
      <animateMotion dur="{snake_dur}s" repeatCount="indefinite" begin="{dt2}" path="{snake_path_d}" />
    </rect>
    <!-- Body Segment 1 -->
    <rect x="-6" y="-6" width="12" height="12" rx="3" fill="#39D353">
      <animateMotion dur="{snake_dur}s" repeatCount="indefinite" begin="{dt1}" path="{snake_path_d}" />
    </rect>
    <!-- Snake Head with expressive pixel eyes -->
    <g>
      <rect x="-6" y="-6" width="12" height="12" rx="3" fill="#69F0A0" stroke="#FFFFFF" stroke-width="0.8"/>
      <circle cx="-2.5" cy="-2.5" r="1.3" fill="#080B10"/>
      <circle cx="2.5" cy="-2.5" r="1.3" fill="#080B10"/>
      <circle cx="-2.5" cy="-2.5" r="0.5" fill="#FFFFFF"/>
      <circle cx="2.5" cy="-2.5" r="0.5" fill="#FFFFFF"/>
      <animateMotion dur="{snake_dur}s" repeatCount="indefinite" begin="0s" path="{snake_path_d}" />
    </g>
  </g>''')

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
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated GitHub contribution heatmap with roaming snake for Zaid7829">
  <title>Zaid7829 — Contribution Heatmap</title>
  <desc>Public contribution calendar for Zaid7829 with 30+ organic glowing cells and roaming snake</desc>
{chr(10).join(parts)}
</svg>
'''
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(svg.encode('utf-8'))/1024:.1f} KB)")

if __name__ == "__main__":
    main()
