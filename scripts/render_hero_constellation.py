"""Renders hero-constellation.svg for Zaid's visual-first developer portfolio."""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "hero-constellation.svg"

# Constellation nodes around center
NODES = [
    {"name": "React", "color": "#61DAFB", "angle": 0, "r": 280, "icon": "⚛️"},
    {"name": "TypeScript", "color": "#3178C6", "angle": 30, "r": 180, "icon": "TS"},
    {"name": "Next.js", "color": "#FFFFFF", "angle": 60, "r": 340, "icon": "▲"},
    {"name": "Node.js", "color": "#339933", "angle": 110, "r": 220, "icon": "⬢"},
    {"name": "Python", "color": "#3776AB", "angle": 140, "r": 320, "icon": "🐍"},
    {"name": "PostgreSQL", "color": "#4169E1", "angle": 175, "r": 200, "icon": "🐘"},
    {"name": "Docker", "color": "#2496ED", "angle": 210, "r": 330, "icon": "🐳"},
    {"name": "Redis", "color": "#DC382D", "angle": 250, "r": 190, "icon": "⚡"},
    {"name": "MongoDB", "color": "#47A248", "angle": 285, "r": 320, "icon": "🍃"},
    {"name": "Git / GitHub", "color": "#F05032", "angle": 325, "r": 210, "icon": "🐙"},
]


def generate_svg() -> str:
    width, height = 940, 300
    cx, cy = width / 2, height / 2

    # Calculate coordinates
    coords = []
    for node in NODES:
        rad = math.radians(node["angle"])
        # Elliptical spread to fit 940x300 canvas
        x = cx + (node["r"] * 1.3) * math.cos(rad)
        y = cy + (node["r"] * 0.42) * math.sin(rad)
        coords.append((node, x, y))

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">',
        """  <defs>
    <radialGradient id="center-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#58A6FF" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#080B10" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="line-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#58A6FF" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#FF8C00" stop-opacity="0.6" />
    </linearGradient>
    <style>
      .const-line { stroke: #30363D; stroke-width: 1; stroke-dasharray: 4, 4; }
      .const-core-line { stroke: url(#line-grad); stroke-width: 1.5; opacity: 0.7; }
      .node-box { fill: #111820; stroke: #30363D; stroke-width: 1; rx: 6px; }
      .node-text { fill: #E6EDF3; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 11px; font-weight: 600; text-anchor: middle; }
      .center-title { fill: #FFFFFF; font-family: ui-monospace, monospace; font-size: 14px; font-weight: 700; letter-spacing: 2px; }
      .center-sub { fill: #58A6FF; font-family: ui-monospace, monospace; font-size: 9px; letter-spacing: 1.5px; }
      @keyframes pulse {
        0%, 100% { r: 3px; opacity: 0.4; }
        50% { r: 5px; opacity: 0.9; }
      }
      .star-dot { fill: #79C0FF; animation: pulse 3s infinite ease-in-out; }
    </style>
  </defs>""",
        f'  <rect width="{width}" height="{height}" fill="#080B10" rx="8" stroke="#30363D" stroke-width="1" />',
        f'  <ellipse cx="{cx}" cy="{cy}" rx="380" ry="120" fill="url(#center-glow)" />',
        f'  <ellipse cx="{cx}" cy="{cy}" rx="360" ry="110" fill="none" stroke="#21262D" stroke-width="1" stroke-dasharray="3, 5" />',
        f'  <ellipse cx="{cx}" cy="{cy}" rx="240" ry="75" fill="none" stroke="#21262D" stroke-width="1" stroke-dasharray="2, 4" />',
    ]

    # Inter-node constellation lines
    for i, (_, x1, y1) in enumerate(coords):
        # Line to center
        svg_parts.append(f'  <line x1="{cx}" y1="{cy}" x2="{x1:.1f}" y2="{y1:.1f}" class="const-core-line" />')
        # Line to neighbor
        next_idx = (i + 1) % len(coords)
        _, x2, y2 = coords[next_idx]
        svg_parts.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="const-line" />')

    # Central Core Node
    core_w, core_h = 220, 52
    svg_parts.extend([
        f'  <g transform="translate({cx - core_w/2}, {cy - core_h/2})">',
        f'    <rect width="{core_w}" height="{core_h}" fill="#161B22" stroke="#58A6FF" stroke-width="1.5" rx="8" />',
        f'    <circle cx="18" cy="{core_h/2}" r="5" fill="#39D353" />',
        f'    <text x="{core_w/2 + 6}" y="23" text-anchor="middle" class="center-title">ZAID // SYSTEM CORE</text>',
        f'    <text x="{core_w/2 + 6}" y="40" text-anchor="middle" class="center-sub">FULL-STACK ENGINE · ONLINE</text>',
        '  </g>',
    ])

    # Orbiting Nodes
    for node, x, y in coords:
        box_w, box_h = 92, 28
        bx, by = x - box_w / 2, y - box_h / 2
        accent = node["color"]
        svg_parts.extend([
            f'  <g transform="translate({bx:.1f}, {by:.1f})">',
            f'    <rect width="{box_w}" height="{box_h}" class="node-box" />',
            f'    <rect width="3" height="{box_h}" fill="{accent}" rx="1" />',
            f'    <text x="14" y="18" font-size="11" fill="{accent}">{node["icon"]}</text>',
            f'    <text x="52" y="18" class="node-text">{node["name"]}</text>',
            '  </g>',
        ])

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def main():
    svg_content = generate_svg()
    OUTPUT.write_text(svg_content, encoding="utf-8")
    print(f"[OK] Generated {OUTPUT.name} ({len(svg_content)} bytes)")


if __name__ == "__main__":
    main()
