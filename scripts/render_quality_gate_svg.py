"""Renders quality-gate.svg circular/radial quality visualization for Zaid's portfolio."""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "quality-gate.svg"

CHECKS = [
    {"name": "GENUINE PROBLEM", "icon": "🎯", "angle": 270},
    {"name": "CLEAN ARCHITECTURE", "icon": "📐", "angle": 315},
    {"name": "FULL-STACK REPO", "icon": "🌐", "angle": 0},
    {"name": "DOCUMENTATION", "icon": "📝", "angle": 45},
    {"name": "ZERO LEAK SECRETS", "icon": "🔒", "angle": 90},
    {"name": "DEFENSIVE VALIDATION", "icon": "🛡️", "angle": 135},
    {"name": "AUTOMATED TESTS", "icon": "🧪", "angle": 180},
    {"name": "LIVE DEPLOYMENT", "icon": "🚀", "angle": 225},
]


def generate_svg() -> str:
    width, height = 940, 360
    cx, cy = width / 2, height / 2
    radius_x, radius_y = 350, 120

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">',
        """  <defs>
    <radialGradient id="q-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#39D353" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#080B10" stop-opacity="0" />
    </radialGradient>
    <style>
      .bg { fill: #080B10; stroke: #30363D; stroke-width: 1; rx: 8px; }
      .spoke { stroke: #30363D; stroke-width: 1.5; stroke-dasharray: 4, 4; }
      .node-card { fill: #111820; stroke: #30363D; stroke-width: 1; rx: 6px; }
      .node-text { fill: #E6EDF3; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 11px; font-weight: 600; }
      .check-mark { fill: #39D353; font-family: ui-monospace, monospace; font-size: 13px; font-weight: bold; }
    </style>
  </defs>""",
        f'  <rect width="{width}" height="{height}" class="bg" />',
        f'  <ellipse cx="{cx}" cy="{cy}" rx="{radius_x}" ry="{radius_y}" fill="url(#q-glow)" />',
        f'  <ellipse cx="{cx}" cy="{cy}" rx="{radius_x}" ry="{radius_y}" fill="none" stroke="#21262D" stroke-width="1.5" stroke-dasharray="3, 5" />',
    ]

    # Calculate coordinates
    coords = []
    for item in CHECKS:
        rad = math.radians(item["angle"])
        x = cx + radius_x * math.cos(rad)
        y = cy + radius_y * math.sin(rad)
        coords.append((item, x, y))

    # Spokes
    for _, x, y in coords:
        svg_parts.append(f'  <line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" class="spoke" />')

    # Central Quality Hub
    hub_w, hub_h = 190, 68
    svg_parts.extend([
        f'  <g transform="translate({cx - hub_w/2}, {cy - hub_h/2})">',
        f'    <rect width="{hub_w}" height="{hub_h}" fill="#161B22" stroke="#39D353" stroke-width="1.5" rx="10" />',
        '    <circle cx="20" cy="22" r="5" fill="#39D353" />',
        '    <text x="32" y="26" fill="#FFFFFF" font-family="ui-monospace, monospace" font-size="12px" font-weight="bold">QUALITY GATE</text>',
        '    <text x="20" y="44" fill="#39D353" font-family="ui-monospace, monospace" font-size="11px" font-weight="bold">8 / 8 CHECKS PASSED</text>',
        '    <text x="20" y="58" fill="#8B949E" font-family="ui-monospace, monospace" font-size="9px">SYSTEM LEVEL: PRODUCTION</text>',
        '  </g>',
    ])

    # Surrounding Check Nodes
    for item, x, y in coords:
        box_w, box_h = 160, 32
        bx, by = x - box_w / 2, y - box_h / 2
        svg_parts.extend([
            f'  <g transform="translate({bx:.1f}, {by:.1f})">',
            f'    <rect width="{box_w}" height="{box_h}" class="node-card" stroke="#238636" />',
            f'    <rect width="3" height="{box_h}" fill="#39D353" rx="1" />',
            f'    <text x="12" y="21" class="check-mark">✓</text>',
            f'    <text x="26" y="21" font-size="12">{item["icon"]}</text>',
            f'    <text x="46" y="20" class="node-text">{item["name"]}</text>',
            '  </g>',
        ])

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def main():
    svg = generate_svg()
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"[OK] Generated {OUTPUT.name} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
