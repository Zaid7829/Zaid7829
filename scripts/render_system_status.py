#!/usr/bin/env python3
"""
Generate a unified terminal system-status SVG.
Output: system-status.svg (940x250)
"""
from __future__ import annotations
import html
from pathlib import Path

OUTPUT_FILE = Path("system-status.svg")
W, H = 940, 250

def esc(text: str) -> str:
    return html.escape(str(text), quote=True)

def render_system_status():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Zaid7829 system status panel">')
    lines.append('  <title>Zaid7829 — System Status</title>')
    lines.append('  <desc>Current technical focus: building, learning, and exploring</desc>')
    
    # Outer Terminal Frame
    lines.append(f'  <rect width="{W}" height="{H}" rx="16" fill="#080B10"/>')
    lines.append(f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="#30363D" stroke-width="1.2"/>')
    
    # Terminal Title Bar
    lines.append(f'  <rect x="1" y="1" width="{W-2}" height="40" rx="15" fill="#0D1117"/>')
    lines.append(f'  <line x1="1" y1="41" x2="{W-1}" y2="41" stroke="#21262D" stroke-width="1"/>')
    lines.append('  <circle cx="22" cy="21" r="5" fill="#FF5F56"/>')
    lines.append('  <circle cx="38" cy="21" r="5" fill="#FFBD2E"/>')
    lines.append('  <circle cx="54" cy="21" r="5" fill="#27C93F"/>')
    lines.append('  <text x="76" y="25" fill="#8B949E" font-family="monospace" font-size="12">zaid@github:~$ ./system --status --verbose</text>')
    lines.append(f'  <text x="{W-24}" y="25" text-anchor="end" fill="#39D353" font-family="monospace" font-size="11">● STATE: ACTIVE // DEV_OS</text>')
    
    # 3 Columns
    col_w = 282
    gap = 14
    start_x = 24
    box_y = 56
    box_h = 138
    
    columns = [
        {
            "title": "CURRENTLY BUILDING",
            "color": "#FF8C00",
            "items": [
                "Full-stack web applications",
                "Resilient REST / WebSocket APIs",
                "Developer automation & tooling",
                "Modular UI component systems"
            ]
        },
        {
            "title": "CURRENTLY LEARNING",
            "color": "#58A6FF",
            "items": [
                "Distributed system architecture",
                "Cloud infra & container orchestration",
                "Structured AI & LLM workflows",
                "Performance & latency profiling"
            ]
        },
        {
            "title": "CURRENTLY EXPLORING",
            "color": "#39D353",
            "items": [
                "Modern developer experience (DX)",
                "Security-by-default architecture",
                "Automated release pipelines",
                "Scalable data modeling"
            ]
        }
    ]
    
    for i, col in enumerate(columns):
        cx = start_x + i * (col_w + gap)
        lines.append(f'  <!-- Panel: {col["title"]} -->')
        lines.append(f'  <rect x="{cx}" y="{box_y}" width="{col_w}" height="{box_h}" rx="8" fill="#0D1117" stroke="#21262D" stroke-width="1"/>')
        lines.append(f'  <circle cx="{cx+16}" cy="{box_y+18}" r="3.5" fill="{col["color"]}"/>')
        lines.append(f'  <text x="{cx+28}" y="{box_y+21}" fill="{col["color"]}" font-family="monospace" font-size="11" font-weight="700">{col["title"]}</text>')
        lines.append(f'  <line x1="{cx+14}" y1="{box_y+32}" x2="{cx+col_w-14}" y2="{box_y+32}" stroke="#21262D" stroke-width="1"/>')
        
        for j, item in enumerate(col["items"]):
            iy = box_y + 52 + j * 22
            lines.append(f'  <text x="{cx+16}" y="{iy}" fill="#FF8C00" font-family="monospace" font-size="10">❯</text>')
            lines.append(f'  <text x="{cx+28}" y="{iy}" fill="#E6EDF3" font-family="monospace" font-size="10">{esc(item)}</text>')
            
    # Bottom Status Line
    lines.append(f'  <!-- Terminal Footer -->')
    lines.append(f'  <line x1="20" y1="{H-36}" x2="{W-20}" y2="{H-36}" stroke="#21262D" stroke-width="1"/>')
    lines.append(f'  <circle cx="28" cy="{H-18}" r="4" fill="#FF8C00"/>')
    lines.append(f'  <text x="40" y="{H-15}" fill="#8B949E" font-family="monospace" font-size="10.5">TARGET: "Turn good ideas into reliable, understandable software people actually want to use."</text>')
    lines.append(f'  <text x="{W-24}" y="{H-15}" text-anchor="end" fill="#6E7681" font-family="monospace" font-size="10.5">CYCLE: ITERATIVE</text>')
    
    lines.append('</svg>')
    
    svg_content = "\n".join(lines)
    OUTPUT_FILE.write_text(svg_content, encoding="utf-8")
    print(f"Rendered {OUTPUT_FILE} ({len(svg_content.encode('utf-8')) / 1024:.1f} KB)")

if __name__ == "__main__":
    render_system_status()
