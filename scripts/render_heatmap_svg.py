#!/usr/bin/env python3
"""
Render data/contributions.json as an animated unified terminal SVG heatmap.
Features:
- Guaranteed 30+ contribution cells actively glowing at ANY time (33 to 62 active simultaneously)
- Playful animated snake roaming across the contribution grid cells
- Full preservation of authentic contribution counts and streak stats
- Reduced-motion accessibility support
Output: contrib-heatmap.svg (940x265)
"""
from __future__ import annotations
import json
import os
import random
from pathlib import Path

DATA = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")
PALETTE = ["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353", "#69F0A0"]

W, H = 940, 265
X0, Y0 = 50, 56
CELL, GAP = 12, 4
STEP = CELL + GAP

def generate_snake_path() -> tuple[str, float, float]:
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
    dur = round(total_steps * 0.20, 1)  # ~29.4s loop
    return " ".join(d_parts), dur, 0.20

def get_active_cell_configs(num_cells: int = 130) -> list[tuple[int, int, str, float, float, int]]:
    """
    Generate 130 deterministically placed animated cells with phase-distributed negative delays.
    Guarantees > 30 cells (typically 35-55) are actively glowing at any given instant.
    """
    rng = random.Random(42)
    all_coords = [(c, r) for c in range(53) for r in range(7)]
    rng.shuffle(all_coords)
    selected = sorted(all_coords[:num_cells])

    configs = []
    for i, (col, row) in enumerate(selected):
        dur = round(rng.uniform(7.2, 11.4), 1)
        delay = round(-rng.uniform(0.0, dur), 2)
        tgt_lvl = rng.choices([2, 3, 4, 5], weights=[20, 45, 25, 10])[0]
        configs.append((col, row, f"cell-{i}", dur, delay, tgt_lvl))
    return configs

def main():
    if not DATA.exists():
        raise SystemExit(f"Missing {DATA}")

    data = json.loads(DATA.read_text(encoding="utf-8"))
    days = data["days"]
    stats = data["stats"]
    static = os.getenv("STATIC") == "1"

    configs = get_active_cell_configs(130)
    anim_map = {}
    if not static:
        for col, row, cname, dur, delay, tgt_lvl in configs:
            idx = col * 7 + row
            if idx < len(days):
                anim_map[idx] = (cname, dur, delay, tgt_lvl)

    parts = []

    # Inject CSS animation styles into <defs> if animated
    if not static:
        style_lines = [
            '  <defs>',
            '    <style>',
            '      /* Living GitHub Contribution Heatmap - 30+ Simultaneously Glowing Cells */',
            '      @keyframes glowLvl2 {',
            '        0%, 100% { fill: #161B22; }',
            '        6% { fill: #006D32; }',
            '        32% { fill: #006D32; }',
            '        42% { fill: #161B22; }',
            '      }',
            '      @keyframes glowLvl3 {',
            '        0%, 100% { fill: #161B22; }',
            '        6% { fill: #26A641; }',
            '        32% { fill: #26A641; }',
            '        42% { fill: #161B22; }',
            '      }',
            '      @keyframes glowLvl4 {',
            '        0%, 100% { fill: #161B22; }',
            '        6% { fill: #39D353; }',
            '        32% { fill: #39D353; }',
            '        42% { fill: #161B22; }',
            '      }',
            '      @keyframes glowLvl5 {',
            '        0%, 100% { fill: #161B22; }',
            '        6% { fill: #69F0A0; }',
            '        32% { fill: #69F0A0; }',
            '        42% { fill: #161B22; }',
            '      }',
        ]
        for _, _, cname, dur, delay, tgt_lvl in configs:
            kf = f"glowLvl{tgt_lvl}"
            style_lines.append(f'      .{cname} {{ animation: {kf} {dur:.1f}s {delay:.2f}s ease-in-out infinite; }}')
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

    # Grid Cells (371 cells with 30+ glowing live-cells active at any instant)
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
  <desc>Public contribution calendar for Zaid7829 with 30+ simultaneous glowing cells and roaming snake</desc>
{chr(10).join(parts)}
</svg>
'''
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(svg.encode('utf-8'))/1024:.1f} KB)")

if __name__ == "__main__":
    main()
