#!/usr/bin/env python3
"""
Generate an animated dark terminal skill radar SVG from data/skills.json.
Output: skill-radar.svg (940x440)
"""
from __future__ import annotations
import json
import math
from pathlib import Path

DATA_FILE = Path("data/skills.json")
OUTPUT_FILE = Path("skill-radar.svg")

def get_polygon_points(center_x: float, center_y: float, radius: float, values: list[float]) -> list[tuple[float, float]]:
    n = len(values)
    points = []
    for i, val in enumerate(values):
        angle = -math.pi / 2 + (2 * math.pi * i / n)
        r = radius * (val / 100.0)
        px = center_x + r * math.cos(angle)
        py = center_y + r * math.sin(angle)
        points.append((px, py))
    return points

def get_web_points(center_x: float, center_y: float, radius: float, n: int, ratio: float) -> list[tuple[float, float]]:
    points = []
    for i in range(n):
        angle = -math.pi / 2 + (2 * math.pi * i / n)
        r = radius * ratio
        px = center_x + r * math.cos(angle)
        py = center_y + r * math.sin(angle)
        points.append((px, py))
    return points

def render_radar():
    if not DATA_FILE.exists():
        raise SystemExit(f"Missing {DATA_FILE}")
        
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    radars = data.get("radars", {})
    disclaimer = data.get("_disclaimer", "Self-assessed development focus — not an objective proficiency score.")
    
    SVG_W = 940
    SVG_H = 440
    
    chart1_data = radars.get("full_stack", {})
    chart2_data = radars.get("language_mix", {})
    
    c1_skills = chart1_data.get("skills", {})
    c2_skills = chart2_data.get("skills", {})
    
    c1_keys = list(c1_skills.keys())
    c1_vals = [float(c1_skills[k]) for k in c1_keys]
    
    c2_keys = list(c2_skills.keys())
    c2_vals = [float(c2_skills[k]) for k in c2_keys]
    
    RADIUS = 104.0
    CENTER1_X = 250.0
    CENTER1_Y = 230.0
    
    CENTER2_X = 690.0
    CENTER2_Y = 230.0
    
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}" role="img" aria-label="Zaid7829 skill radar visualization">')
    lines.append('  <title>Zaid7829 — Technical Capability Radar</title>')
    lines.append(f'  <desc>{disclaimer}</desc>')
    
    # Styles
    lines.append('  <style>')
    lines.append('    @keyframes radarScale {')
    lines.append('      0% { opacity: 0; transform: scale(0.2); }')
    lines.append('      60% { opacity: 0.8; }')
    lines.append('      100% { opacity: 1; transform: scale(1); }')
    lines.append('    }')
    lines.append('    @keyframes fadeIn {')
    lines.append('      0% { opacity: 0; }')
    lines.append('      100% { opacity: 1; }')
    lines.append('    }')
    lines.append(f'    .poly-left {{ transform-origin: {CENTER1_X}px {CENTER1_Y}px; animation: radarScale 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.35s forwards; }}')
    lines.append(f'    .poly-right {{ transform-origin: {CENTER2_X}px {CENTER2_Y}px; animation: radarScale 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.50s forwards; }}')
    lines.append('    .axis-label { font-family: monospace; font-size: 10px; fill: #C9D1D9; }')
    lines.append('    .axis-sub { font-family: monospace; font-size: 9px; fill: #8B949E; }')
    lines.append('  </style>')
    
    # Gradients
    lines.append('  <defs>')
    lines.append('    <radialGradient id="gradOrange" cx="50%" cy="50%" r="50%">')
    lines.append('      <stop offset="0%" stop-color="#FF8C00" stop-opacity="0.32"/>')
    lines.append('      <stop offset="100%" stop-color="#FF8C00" stop-opacity="0.06"/>')
    lines.append('    </radialGradient>')
    lines.append('    <radialGradient id="gradBlue" cx="50%" cy="50%" r="50%">')
    lines.append('      <stop offset="0%" stop-color="#58A6FF" stop-opacity="0.32"/>')
    lines.append('      <stop offset="100%" stop-color="#58A6FF" stop-opacity="0.06"/>')
    lines.append('    </radialGradient>')
    lines.append('  </defs>')
    
    # Outer Terminal Frame
    lines.append(f'  <rect width="{SVG_W}" height="{SVG_H}" rx="16" fill="#080B10"/>')
    lines.append(f'  <rect x="1" y="1" width="{SVG_W-2}" height="{SVG_H-2}" rx="15" fill="none" stroke="#30363D" stroke-width="1.2"/>')
    
    # Terminal Title Bar
    lines.append(f'  <rect x="1" y="1" width="{SVG_W-2}" height="40" rx="15" fill="#0D1117"/>')
    lines.append(f'  <line x1="1" y1="41" x2="{SVG_W-1}" y2="41" stroke="#21262D" stroke-width="1"/>')
    lines.append('  <circle cx="22" cy="21" r="5" fill="#FF5F56"/>')
    lines.append('  <circle cx="38" cy="21" r="5" fill="#FFBD2E"/>')
    lines.append('  <circle cx="54" cy="21" r="5" fill="#27C93F"/>')
    lines.append('  <text x="76" y="25" fill="#8B949E" font-family="monospace" font-size="12">zaid@github:~$ ./radar --view focus --self-assessed</text>')
    lines.append(f'  <text x="{SVG_W-24}" y="25" text-anchor="end" fill="#6E7681" font-family="monospace" font-size="11">DUAL_RADAR // SELF_ASSESSED</text>')
    
    # Divider line between two charts
    lines.append(f'  <line x1="{SVG_W/2}" y1="52" x2="{SVG_W/2}" y2="{SVG_H-48}" stroke="#21262D" stroke-dasharray="4,4" stroke-width="1"/>')
    
    # RENDER CHART 1 (Full Stack Focus)
    lines.append('  <!-- Chart 1: Full Stack -->')
    lines.append(f'  <text x="{CENTER1_X}" y="68" text-anchor="middle" fill="#FF8C00" font-family="monospace" font-size="13" font-weight="700">~/ full stack development focus</text>')
    lines.append(f'  <text x="{CENTER1_X}" y="84" text-anchor="middle" fill="#8B949E" font-family="monospace" font-size="10">Self-assessed focus &amp; time distribution across stack layers</text>')
    
    # Grid rings
    n1 = len(c1_keys)
    for ratio in [0.2, 0.4, 0.6, 0.8, 1.0]:
        web_pts = get_web_points(CENTER1_X, CENTER1_Y, RADIUS, n1, ratio)
        pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in web_pts)
        stroke_color = "#30363D" if ratio == 1.0 else "#1F242C"
        lines.append(f'  <polygon points="{pts_str}" fill="none" stroke="{stroke_color}" stroke-width="1"/>')
        
    # Spokes and Labels
    outer_pts1 = get_web_points(CENTER1_X, CENTER1_Y, RADIUS, n1, 1.0)
    for i, (ox, oy) in enumerate(outer_pts1):
        lines.append(f'  <line x1="{CENTER1_X}" y1="{CENTER1_Y}" x2="{ox:.1f}" y2="{oy:.1f}" stroke="#21262D" stroke-width="1"/>')
        angle = -math.pi / 2 + (2 * math.pi * i / n1)
        lx = CENTER1_X + (RADIUS + 22.0) * math.cos(angle)
        ly = CENTER1_Y + (RADIUS + 16.0) * math.sin(angle)
        
        anchor = "middle"
        if math.cos(angle) > 0.25:
            anchor = "start"
            lx += 4
        elif math.cos(angle) < -0.25:
            anchor = "end"
            lx -= 4
            
        lines.append(f'  <text x="{lx:.1f}" y="{ly+3:.1f}" text-anchor="{anchor}" class="axis-label">{c1_keys[i]}</text>')
        lines.append(f'  <text x="{lx:.1f}" y="{ly+14:.1f}" text-anchor="{anchor}" class="axis-sub">{int(c1_vals[i])}%</text>')
        
    # Value Polygon 1
    poly1_pts = get_polygon_points(CENTER1_X, CENTER1_Y, RADIUS, c1_vals)
    pts1_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in poly1_pts)
    lines.append(f'  <g class="poly-left" opacity="0">')
    lines.append(f'    <polygon points="{pts1_str}" fill="url(#gradOrange)" stroke="#FF8C00" stroke-width="1.8"/>')
    for px, py in poly1_pts:
        lines.append(f'    <circle cx="{px:.1f}" cy="{py:.1f}" r="3.2" fill="#FFD166" stroke="#080B10" stroke-width="1"/>')
    lines.append('  </g>')
    
    # RENDER CHART 2 (Language Mix)
    lines.append('  <!-- Chart 2: Language Mix -->')
    lines.append(f'  <text x="{CENTER2_X}" y="68" text-anchor="middle" fill="#58A6FF" font-family="monospace" font-size="13" font-weight="700">~/ core languages &amp; systems</text>')
    lines.append(f'  <text x="{CENTER2_X}" y="84" text-anchor="middle" fill="#8B949E" font-family="monospace" font-size="10">Familiarity &amp; usage frequency across core languages</text>')
    
    n2 = len(c2_keys)
    for ratio in [0.2, 0.4, 0.6, 0.8, 1.0]:
        web_pts = get_web_points(CENTER2_X, CENTER2_Y, RADIUS, n2, ratio)
        pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in web_pts)
        stroke_color = "#30363D" if ratio == 1.0 else "#1F242C"
        lines.append(f'  <polygon points="{pts_str}" fill="none" stroke="{stroke_color}" stroke-width="1"/>')
        
    outer_pts2 = get_web_points(CENTER2_X, CENTER2_Y, RADIUS, n2, 1.0)
    for i, (ox, oy) in enumerate(outer_pts2):
        lines.append(f'  <line x1="{CENTER2_X}" y1="{CENTER2_Y}" x2="{ox:.1f}" y2="{oy:.1f}" stroke="#21262D" stroke-width="1"/>')
        angle = -math.pi / 2 + (2 * math.pi * i / n2)
        lx = CENTER2_X + (RADIUS + 22.0) * math.cos(angle)
        ly = CENTER2_Y + (RADIUS + 16.0) * math.sin(angle)
        
        anchor = "middle"
        if math.cos(angle) > 0.25:
            anchor = "start"
            lx += 4
        elif math.cos(angle) < -0.25:
            anchor = "end"
            lx -= 4
            
        lines.append(f'  <text x="{lx:.1f}" y="{ly+3:.1f}" text-anchor="{anchor}" class="axis-label">{c2_keys[i]}</text>')
        lines.append(f'  <text x="{lx:.1f}" y="{ly+14:.1f}" text-anchor="{anchor}" class="axis-sub">{int(c2_vals[i])}%</text>')
        
    # Value Polygon 2
    poly2_pts = get_polygon_points(CENTER2_X, CENTER2_Y, RADIUS, c2_vals)
    pts2_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in poly2_pts)
    lines.append(f'  <g class="poly-right" opacity="0">')
    lines.append(f'    <polygon points="{pts2_str}" fill="url(#gradBlue)" stroke="#58A6FF" stroke-width="1.8"/>')
    for px, py in poly2_pts:
        lines.append(f'    <circle cx="{px:.1f}" cy="{py:.1f}" r="3.2" fill="#79C0FF" stroke="#080B10" stroke-width="1"/>')
    lines.append('  </g>')
    
    # Terminal Bottom Legend & Disclaimer Bar
    lines.append('  <!-- Terminal Footer / Disclaimer -->')
    lines.append(f'  <line x1="20" y1="{SVG_H-40}" x2="{SVG_W-20}" y2="{SVG_H-40}" stroke="#21262D" stroke-width="1"/>')
    lines.append(f'  <circle cx="32" cy="{SVG_H-20}" r="4" fill="#FF8C00"/>')
    lines.append(f'  <text x="44" y="{SVG_H-17}" fill="#E6EDF3" font-family="monospace" font-size="10.5">Full Stack Focus</text>')
    lines.append(f'  <circle cx="165" cy="{SVG_H-20}" r="4" fill="#58A6FF"/>')
    lines.append(f'  <text x="177" y="{SVG_H-17}" fill="#E6EDF3" font-family="monospace" font-size="10.5">Languages &amp; Systems</text>')
    lines.append(f'  <text x="{SVG_W-24}" y="{SVG_H-17}" text-anchor="end" fill="#8B949E" font-family="monospace" font-size="10.5">ℹ {disclaimer}</text>')
    
    lines.append('</svg>')
    
    svg_content = "\n".join(lines)
    OUTPUT_FILE.write_text(svg_content, encoding="utf-8")
    print(f"Rendered {OUTPUT_FILE} ({len(svg_content.encode('utf-8')) / 1024:.1f} KB)")

if __name__ == "__main__":
    render_radar()
