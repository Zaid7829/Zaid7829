"""Renders workflow-pipeline.svg for Zaid's visual-first developer portfolio."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "workflow-pipeline.svg"

STAGES = [
    {"num": "01", "name": "IDEATE", "icon": "💡", "color": "#FFD166"},
    {"num": "02", "name": "DESIGN", "icon": "🎨", "color": "#58A6FF"},
    {"num": "03", "name": "CODE", "icon": "💻", "color": "#79C0FF"},
    {"num": "04", "name": "TEST", "icon": "🧪", "color": "#39D353"},
    {"num": "05", "name": "REVIEW", "icon": "🔍", "color": "#A371F7"},
    {"num": "06", "name": "DEPLOY", "icon": "🚀", "color": "#FF8C00"},
    {"num": "07", "name": "MONITOR", "icon": "📊", "color": "#2EA043"},
    {"num": "08", "name": "REFINE", "icon": "🔄", "color": "#58A6FF"},
]


def generate_svg() -> str:
    width, height = 940, 160
    n = len(STAGES)
    box_w, box_h = 92, 90
    margin_x = 35
    available_w = width - 2 * margin_x
    step_x = available_w / (n - 1)
    cy = height / 2 + 10

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">',
        """  <defs>
    <style>
      .bg { fill: #080B10; stroke: #30363D; stroke-width: 1; rx: 8px; }
      .pipe-line { stroke: #30363D; stroke-width: 2; }
      .flow-pulse { stroke: #58A6FF; stroke-width: 2; stroke-dasharray: 6, 8; animation: flow 15s linear infinite; }
      .card { fill: #111820; stroke: #30363D; stroke-width: 1; rx: 8px; }
      .card-num { fill: #8B949E; font-family: ui-monospace, monospace; font-size: 9px; font-weight: bold; }
      .card-title { fill: #E6EDF3; font-family: ui-monospace, monospace; font-size: 10px; font-weight: bold; text-anchor: middle; }
      @keyframes flow {
        to { stroke-dashoffset: -500; }
      }
    </style>
  </defs>""",
        f'  <rect width="{width}" height="{height}" class="bg" />',
        '  <text x="24" y="24" fill="#8B949E" font-family="ui-monospace, monospace" font-size="11px">~/ 09. developer-workflow // CONTINUOUS DELIVERY PIPELINE</text>',
        '  <text x="916" y="24" fill="#39D353" font-family="ui-monospace, monospace" font-size="11px" text-anchor="end">AUTOMATED CI/CD ●</text>',
    ]

    # Main connector line behind boxes
    svg_parts.append(f'  <line x1="{margin_x}" y1="{cy}" x2="{width - margin_x}" y2="{cy}" class="pipe-line" />')
    svg_parts.append(f'  <line x1="{margin_x}" y1="{cy}" x2="{width - margin_x}" y2="{cy}" class="flow-pulse" />')

    # Stage cards
    for i, stage in enumerate(STAGES):
        center_x = margin_x + i * step_x
        bx = center_x - box_w / 2
        by = cy - box_h / 2
        accent = stage["color"]

        svg_parts.extend([
            f'  <g transform="translate({bx:.1f}, {by:.1f})">',
            f'    <rect width="{box_w}" height="{box_h}" class="card" />',
            f'    <rect width="{box_w}" height="3" fill="{accent}" rx="1" />',
            f'    <text x="10" y="18" class="card-num">{stage["num"]}</text>',
            f'    <text x="{box_w/2}" y="48" font-size="22" text-anchor="middle">{stage["icon"]}</text>',
            f'    <text x="{box_w/2}" y="74" class="card-title">{stage["name"]}</text>',
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
