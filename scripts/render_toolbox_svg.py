#!/usr/bin/env python3
"""
Generate a self-contained, unified visual developer toolbox SVG with real official SVG logos.
Features:
- Visual-first logos (32x32px) as primary elements
- 6 standard categories: LANGUAGES, FRONTEND, BACKEND & APIS, DATABASES, DEVOPS & CLOUD, TESTING & QA
- Zero emojis, real SVG vector paths
- Dark terminal aesthetic with window chrome and monospace headings
- Interactive CSS hover: scale 1.08, brand drop-shadow glow, logo brightening, custom tooltips
- Accessible roles, labels, and titles
Output: toolbox.svg (940x670)
"""
from __future__ import annotations
import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

OUTPUT_FILE = Path("toolbox.svg")
ICONS_DIR = Path("icons")

CATEGORIES = [
    {
        "id": "01",
        "name": "LANGUAGES",
        "color": "#FF8C00",
        "tag": "CORE_SYNTAX",
        "items": [
            {"name": "TypeScript", "key": "typescript", "label": "TypeScript"},
            {"name": "JavaScript", "key": "javascript", "label": "JavaScript"},
            {"name": "Python", "key": "python", "label": "Python"},
            {"name": "Go", "key": "go", "label": "Go"},
            {"name": "Rust", "key": "rust", "label": "Rust"},
            {"name": "Java", "key": "java", "label": "Java"},
            {"name": "C++", "key": "cplusplus", "label": "C++"},
            {"name": "SQL", "key": "sql", "label": "SQL"},
            {"name": "Bash", "key": "bash", "label": "Bash"}
        ]
    },
    {
        "id": "02",
        "name": "FRONTEND",
        "color": "#38BDF8",
        "tag": "CLIENT_ENGINEERING",
        "items": [
            {"name": "React", "key": "react", "label": "React"},
            {"name": "Next.js", "key": "nextjs", "label": "Next.js"},
            {"name": "Tailwind CSS", "key": "tailwindcss", "label": "Tailwind"},
            {"name": "Vue", "key": "vue", "label": "Vue"},
            {"name": "Angular", "key": "angular", "label": "Angular"},
            {"name": "Svelte", "key": "svelte", "label": "Svelte"},
            {"name": "Vite", "key": "vite", "label": "Vite"},
            {"name": "HTML5", "key": "html5", "label": "HTML5"},
            {"name": "CSS3", "key": "css3", "label": "CSS3"}
        ]
    },
    {
        "id": "03",
        "name": "BACKEND & APIS",
        "color": "#58A6FF",
        "tag": "SERVICES_ROUTING",
        "items": [
            {"name": "Node.js", "key": "nodejs", "label": "Node.js"},
            {"name": "FastAPI", "key": "fastapi", "label": "FastAPI"},
            {"name": "Express", "key": "express", "label": "Express"},
            {"name": "NestJS", "key": "nestjs", "label": "NestJS"},
            {"name": "Django", "key": "django", "label": "Django"},
            {"name": "Flask", "key": "flask", "label": "Flask"},
            {"name": "REST", "key": "rest", "label": "REST API"},
            {"name": "GraphQL", "key": "graphql", "label": "GraphQL"}
        ]
    },
    {
        "id": "04",
        "name": "DATABASES",
        "color": "#3FB950",
        "tag": "PERSISTENCE_CACHE",
        "items": [
            {"name": "PostgreSQL", "key": "postgresql", "label": "PostgreSQL"},
            {"name": "MongoDB", "key": "mongodb", "label": "MongoDB"},
            {"name": "Redis", "key": "redis", "label": "Redis"},
            {"name": "MySQL", "key": "mysql", "label": "MySQL"},
            {"name": "SQLite", "key": "sqlite", "label": "SQLite"},
            {"name": "Prisma ORM", "key": "prisma", "label": "Prisma"},
            {"name": "SQLAlchemy", "key": "sqlalchemy", "label": "SQLAlchemy"}
        ]
    },
    {
        "id": "05",
        "name": "DEVOPS & CLOUD",
        "color": "#A371F7",
        "tag": "INFRA_PIPELINE",
        "items": [
            {"name": "Docker", "key": "docker", "label": "Docker"},
            {"name": "Kubernetes", "key": "kubernetes", "label": "Kubernetes"},
            {"name": "GitHub Actions", "key": "githubactions", "label": "GH Actions"},
            {"name": "AWS", "key": "aws", "label": "AWS"},
            {"name": "Azure", "key": "azure", "label": "Azure"},
            {"name": "Linux", "key": "linux", "label": "Linux"}
        ]
    },
    {
        "id": "06",
        "name": "TESTING & QA",
        "color": "#F85149",
        "tag": "VERIFICATION_SUITE",
        "items": [
            {"name": "Jest", "key": "jest", "label": "Jest"},
            {"name": "Vitest", "key": "vitest", "label": "Vitest"},
            {"name": "Pytest", "key": "pytest", "label": "Pytest"},
            {"name": "Playwright", "key": "playwright", "label": "Playwright"},
            {"name": "Cypress", "key": "cypress", "label": "Cypress"},
            {"name": "Testing Library", "key": "testinglibrary", "label": "Test Library"}
        ]
    }
]

W, H = 940, 670

def strip_ns(elem):
    if '}' in elem.tag:
        elem.tag = elem.tag.split('}', 1)[1]
    for key, value in list(elem.attrib.items()):
        if '}' in key:
            del elem.attrib[key]
            elem.attrib[key.split('}', 1)[1]] = value
    for child in elem:
        strip_ns(child)

def sanitize_icon_xml(svg_path: Path, tech_key: str):
    """
    Reads an icon SVG, prefixes all internal IDs to avoid collisions,
    and returns viewBox and inner XML elements string.
    """
    content = svg_path.read_text(encoding='utf-8')
    
    # Find all id="..." and prefix them
    ids = re.findall(r'id=["\']([^"\']+)["\']', content)
    for id_val in set(ids):
        prefixed = f"{tech_key}_{id_val}"
        content = re.sub(f'id=["\']{re.escape(id_val)}["\']', f'id="{prefixed}"', content)
        content = re.sub(rf'url\(#{re.escape(id_val)}\)', f'url(#{prefixed})', content)
        content = re.sub(f'href=["\']#{re.escape(id_val)}["\']', f'href="#{prefixed}"', content)
    
    tree = ET.fromstring(content)
    viewBox = tree.get('viewBox')
    if not viewBox:
        w = tree.get('width', '128').replace('px', '')
        h = tree.get('height', '128').replace('px', '')
        viewBox = f"0 0 {w} {h}"
    
    inner_strs = []
    for child in tree:
        strip_ns(child)
        child_str = ET.tostring(child, encoding='unicode')
        inner_strs.append(child_str)
        
    return viewBox, "\n".join(inner_strs)

def render_toolbox():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Zaid7829 developer toolbox and visual technology index">')
    lines.append('  <title>Zaid7829 — Developer Toolbox</title>')
    lines.append('  <desc>Visual technology index featuring official logos across languages, frameworks, cloud, databases, and testing</desc>')
    
    # CSS Styles for interactions
    lines.append('  <style>')
    lines.append('    .tech-card {')
    lines.append('      cursor: pointer;')
    lines.append('      transform-origin: center;')
    lines.append('      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);')
    lines.append('    }')
    lines.append('    .tech-card .card-bg {')
    lines.append('      fill: #0D1117;')
    lines.append('      stroke: #21262D;')
    lines.append('      stroke-width: 1px;')
    lines.append('      transition: all 0.2s ease;')
    lines.append('    }')
    lines.append('    .tech-card .logo-box {')
    lines.append('      opacity: 0.88;')
    lines.append('      transition: all 0.2s ease;')
    lines.append('    }')
    lines.append('    .tech-card .card-label {')
    lines.append('      fill: #8B949E;')
    lines.append('      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;')
    lines.append('      font-size: 9.5px;')
    lines.append('      transition: fill 0.2s ease;')
    lines.append('    }')
    lines.append('    .tech-card .tooltip {')
    lines.append('      opacity: 0;')
    lines.append('      pointer-events: none;')
    lines.append('      transform: translateY(4px);')
    lines.append('      transition: opacity 0.2s ease, transform 0.2s ease;')
    lines.append('    }')
    lines.append('    .tech-card:hover {')
    lines.append('      transform: translateY(-2px) scale(1.06);')
    lines.append('    }')
    lines.append('    .tech-card:hover .card-bg {')
    lines.append('      fill: #161B22;')
    lines.append('      stroke: var(--accent, #58A6FF);')
    lines.append('      filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.4));')
    lines.append('    }')
    lines.append('    .tech-card:hover .logo-box {')
    lines.append('      opacity: 1;')
    lines.append('      filter: drop-shadow(0 0 8px var(--glow, rgba(88, 166, 255, 0.4)));')
    lines.append('    }')
    lines.append('    .tech-card:hover .card-label {')
    lines.append('      fill: #F0F6FC;')
    lines.append('      font-weight: 600;')
    lines.append('    }')
    lines.append('    .tech-card:hover .tooltip {')
    lines.append('      opacity: 1;')
    lines.append('      transform: translateY(0);')
    lines.append('    }')
    lines.append('  </style>')
    
    # Outer Terminal Frame
    lines.append(f'  <rect width="{W}" height="{H}" rx="14" fill="#080B10"/>')
    lines.append(f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13" fill="none" stroke="#30363D" stroke-width="1.2"/>')
    
    # Terminal Title Bar
    lines.append(f'  <rect x="1" y="1" width="{W-2}" height="38" rx="13" fill="#0D1117"/>')
    lines.append(f'  <line x1="1" y1="39" x2="{W-1}" y2="39" stroke="#21262D" stroke-width="1"/>')
    lines.append('  <circle cx="20" cy="20" r="5" fill="#FF5F56"/>')
    lines.append('  <circle cx="36" cy="20" r="5" fill="#FFBD2E"/>')
    lines.append('  <circle cx="52" cy="20" r="5" fill="#27C93F"/>')
    lines.append('  <text x="74" y="24" fill="#8B949E" font-family="ui-monospace, monospace" font-size="12">zaid@github:~$ ./toolbox --visual --cluster</text>')
    lines.append(f'  <text x="{W-24}" y="24" text-anchor="end" fill="#FF8C00" font-family="ui-monospace, monospace" font-size="11" font-weight="600">45 TECHNOLOGIES // VISUAL CLUSTER</text>')
    
    # Section Subheader
    lines.append('  <text x="28" y="66" fill="#FF8C00" font-family="ui-monospace, monospace" font-size="13" font-weight="700">~/ 03. toolbox</text>')
    lines.append('  <text x="140" y="66" fill="#8B949E" font-family="ui-monospace, monospace" font-size="11">Production technology stack and verified engineering capabilities</text>')
    lines.append(f'  <line x1="28" y1="76" x2="{W-28}" y2="76" stroke="#21262D" stroke-width="1"/>')
    
    start_y = 90
    lane_height = 84
    lane_gap = 10
    
    # Layout 6 categories as horizontal architectural clusters
    for cat_idx, cat in enumerate(CATEGORIES):
        cy = start_y + cat_idx * (lane_height + lane_gap)
        color = cat["color"]
        cat_name = cat["name"]
        item_count = len(cat["items"])
        
        # Lane container
        lines.append(f'  <!-- Lane: {cat_name} -->')
        lines.append(f'  <g id="lane-{cat["id"]}">')
        lines.append(f'    <rect x="28" y="{cy}" width="{W-56}" height="{lane_height}" rx="8" fill="#090D13" stroke="#1F242C" stroke-width="1"/>')
        
        # Category Accent Left Bar
        lines.append(f'    <rect x="28" y="{cy}" width="4" height="{lane_height}" rx="2" fill="{color}"/>')
        
        # Category Monospace Header Info
        lines.append(f'    <text x="44" y="{cy+24}" fill="{color}" font-family="ui-monospace, monospace" font-size="11" font-weight="700">[{cat["id"]}] {html.escape(cat_name)}</text>')
        lines.append(f'    <text x="44" y="{cy+42}" fill="#6E7681" font-family="ui-monospace, monospace" font-size="9" font-weight="500">{cat["tag"]}</text>')
        lines.append(f'    <text x="44" y="{cy+60}" fill="#484F58" font-family="ui-monospace, monospace" font-size="9">{item_count} ITEMS</text>')
        lines.append(f'    <line x1="172" y1="{cy+10}" x2="172" y2="{cy+lane_height-10}" stroke="#1F242C" stroke-width="1"/>')
        
        # Items Area (x = 186 to W-38 = 902, total available = 716px)
        items_area_x = 186
        available_w = W - 38 - items_area_x
        
        # Compute item box sizing
        # For 9 items: 72px card width, ~8px gap
        card_w = 70
        card_h = 66
        
        # Space items evenly
        if item_count > 1:
            total_cards_w = item_count * card_w
            gap = (available_w - total_cards_w) / (item_count - 1)
            # cap gap between 8 and 28
            gap = max(8, min(24, gap))
        else:
            gap = 12
            
        for idx, item in enumerate(cat["items"]):
            ix = items_area_x + idx * (card_w + gap)
            iy = cy + (lane_height - card_h) / 2
            
            svg_file = ICONS_DIR / f"{item['key']}.svg"
            if not svg_file.exists():
                print(f"Warning: icon file not found: {svg_file}")
                continue
                
            viewBox, inner_xml = sanitize_icon_xml(svg_file, f"{cat['id']}_{item['key']}")
            
            # Interactive Tech Card
            lines.append(f'    <g class="tech-card" style="--accent: {color}; --glow: {color}66;" role="img" aria-label="{html.escape(item["name"])} - {html.escape(cat_name)}">')
            lines.append(f'      <title>{html.escape(item["name"])} · {html.escape(cat_name)}</title>')
            
            # Card Background
            lines.append(f'      <rect class="card-bg" x="{ix:.1f}" y="{iy:.1f}" width="{card_w}" height="{card_h}" rx="6"/>')
            
            # Nested SVG Logo (30x30 centered horizontally in card)
            logo_size = 30
            logo_x = ix + (card_w - logo_size) / 2
            logo_y = iy + 7
            lines.append(f'      <svg class="logo-box" x="{logo_x:.1f}" y="{logo_y:.1f}" width="{logo_size}" height="{logo_size}" viewBox="{viewBox}">')
            lines.append(inner_xml)
            lines.append('      </svg>')
            
            # Label below logo
            label_y = iy + 53
            lines.append(f'      <text class="card-label" x="{ix + card_w/2:.1f}" y="{label_y:.1f}" text-anchor="middle">{html.escape(item["label"])}</text>')
            
            # Tooltip HUD
            tip_w = max(80, len(item["name"]) * 8 + 20)
            tip_h = 28
            tip_x = ix + (card_w - tip_w) / 2
            tip_y = iy - tip_h - 6
            lines.append('      <g class="tooltip">')
            lines.append(f'        <rect x="{tip_x:.1f}" y="{tip_y:.1f}" width="{tip_w}" height="{tip_h}" rx="5" fill="#161B22" stroke="{color}" stroke-width="1.2" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.6))"/>')
            lines.append(f'        <text x="{tip_x + tip_w/2:.1f}" y="{tip_y + 13:.1f}" text-anchor="middle" fill="#FFFFFF" font-family="ui-monospace, monospace" font-size="9.5" font-weight="700">{html.escape(item["name"])}</text>')
            lines.append(f'        <text x="{tip_x + tip_w/2:.1f}" y="{tip_y + 23:.1f}" text-anchor="middle" fill="#8B949E" font-family="ui-monospace, monospace" font-size="8">{html.escape(cat_name)}</text>')
            lines.append('      </g>')
            
            lines.append('    </g>')
            
        lines.append('  </g>')
        
    lines.append('</svg>')
    
    svg_content = "\n".join(lines)
    OUTPUT_FILE.write_text(svg_content, encoding='utf-8')
    print(f"Generated {OUTPUT_FILE} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    render_toolbox()
