#!/usr/bin/env python3
"""
Generate a self-contained visual developer toolbox SVG.
Specifications:
- Visual-only: NO technology text names visible normally
- Real official SVG logos (48x48px) inside dark grey square containers (76x76px)
- Container background: #252B33, border: #343B45, border-radius: 10px
- Generous spacing: 24px gap between containers
- Category headings: clean, technical, small (e.g. [01] LANGUAGES)
- Interactive hover: subtle border highlight and minimal tooltip with tech name
- Output: toolbox.svg (940x890)
"""
from __future__ import annotations
import html
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
        "items": [
            {"name": "TypeScript", "key": "typescript"},
            {"name": "JavaScript", "key": "javascript"},
            {"name": "Python", "key": "python"},
            {"name": "Go", "key": "go"},
            {"name": "Rust", "key": "rust"},
            {"name": "Java", "key": "java"},
            {"name": "C++", "key": "cplusplus"},
            {"name": "SQL", "key": "sql"},
            {"name": "Bash", "key": "bash"}
        ]
    },
    {
        "id": "02",
        "name": "FRONTEND",
        "color": "#38BDF8",
        "items": [
            {"name": "React", "key": "react"},
            {"name": "Next.js", "key": "nextjs"},
            {"name": "Tailwind CSS", "key": "tailwindcss"},
            {"name": "Vue", "key": "vue"},
            {"name": "Angular", "key": "angular"},
            {"name": "Svelte", "key": "svelte"},
            {"name": "Vite", "key": "vite"},
            {"name": "HTML5", "key": "html5"},
            {"name": "CSS3", "key": "css3"}
        ]
    },
    {
        "id": "03",
        "name": "BACKEND & APIS",
        "color": "#58A6FF",
        "items": [
            {"name": "Node.js", "key": "nodejs"},
            {"name": "FastAPI", "key": "fastapi"},
            {"name": "Express", "key": "express"},
            {"name": "NestJS", "key": "nestjs"},
            {"name": "Django", "key": "django"},
            {"name": "Flask", "key": "flask"},
            {"name": "REST", "key": "rest"},
            {"name": "GraphQL", "key": "graphql"}
        ]
    },
    {
        "id": "04",
        "name": "DATABASES",
        "color": "#3FB950",
        "items": [
            {"name": "PostgreSQL", "key": "postgresql"},
            {"name": "MongoDB", "key": "mongodb"},
            {"name": "Redis", "key": "redis"},
            {"name": "MySQL", "key": "mysql"},
            {"name": "SQLite", "key": "sqlite"},
            {"name": "Prisma ORM", "key": "prisma"},
            {"name": "SQLAlchemy", "key": "sqlalchemy"}
        ]
    },
    {
        "id": "05",
        "name": "DEVOPS & CLOUD",
        "color": "#A371F7",
        "items": [
            {"name": "Docker", "key": "docker"},
            {"name": "Kubernetes", "key": "kubernetes"},
            {"name": "GitHub Actions", "key": "githubactions"},
            {"name": "AWS", "key": "aws"},
            {"name": "Azure", "key": "azure"},
            {"name": "Linux", "key": "linux"}
        ]
    },
    {
        "id": "06",
        "name": "TESTING & QA",
        "color": "#F85149",
        "items": [
            {"name": "Jest", "key": "jest"},
            {"name": "Vitest", "key": "vitest"},
            {"name": "Pytest", "key": "pytest"},
            {"name": "Playwright", "key": "playwright"},
            {"name": "Cypress", "key": "cypress"},
            {"name": "Testing Library", "key": "testinglibrary"}
        ]
    }
]

W, H = 940, 890

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
    content = svg_path.read_text(encoding='utf-8')
    
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
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Zaid developer toolbox and visual technology matrix">')
    lines.append('  <title>Zaid — Developer Toolbox</title>')
    lines.append('  <desc>Visual technology grid featuring official logos inside grey containers without text labels</desc>')
    
    # CSS Styles for interactions
    lines.append('  <style>')
    lines.append('    .icon-container {')
    lines.append('      cursor: pointer;')
    lines.append('      transform-origin: center;')
    lines.append('      transition: transform 0.15s ease;')
    lines.append('    }')
    lines.append('    .icon-container .box-bg {')
    lines.append('      fill: #252B33;')
    lines.append('      stroke: #343B45;')
    lines.append('      stroke-width: 1.2px;')
    lines.append('      transition: fill 0.15s ease, stroke 0.15s ease;')
    lines.append('    }')
    lines.append('    .icon-container .logo-svg {')
    lines.append('      transition: transform 0.15s ease;')
    lines.append('    }')
    lines.append('    .icon-container .tooltip {')
    lines.append('      opacity: 0;')
    lines.append('      pointer-events: none;')
    lines.append('      transform: translateY(3px);')
    lines.append('      transition: opacity 0.15s ease, transform 0.15s ease;')
    lines.append('    }')
    lines.append('    .icon-container:hover {')
    lines.append('      transform: translateY(-2px);')
    lines.append('    }')
    lines.append('    .icon-container:hover .box-bg {')
    lines.append('      fill: #2D333B;')
    lines.append('      stroke: #58A6FF;')
    lines.append('    }')
    lines.append('    .icon-container:hover .logo-svg {')
    lines.append('      transform: scale(1.05);')
    lines.append('      transform-origin: center;')
    lines.append('    }')
    lines.append('    .icon-container:hover .tooltip {')
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
    lines.append('  <text x="74" y="24" fill="#8B949E" font-family="ui-monospace, monospace" font-size="12">zaid@github:~$ ./toolbox --grid --logos-only</text>')
    lines.append(f'  <text x="{W-24}" y="24" text-anchor="end" fill="#8B949E" font-family="ui-monospace, monospace" font-size="11" font-weight="600">ACTIVE_STACK // 44 TECHNOLOGIES</text>')
    
    # Section Title & Subheader
    lines.append('  <text x="32" y="66" fill="#FF8C00" font-family="ui-monospace, monospace" font-size="13" font-weight="700">~/ 03. toolbox</text>')
    lines.append('  <text x="144" y="66" fill="#8B949E" font-family="ui-monospace, monospace" font-size="11">Production technology stack and verified engineering capabilities</text>')
    lines.append(f'  <line x1="32" y1="76" x2="{W-32}" y2="76" stroke="#21262D" stroke-width="1"/>')
    
    # Grid Specifications
    box_size = 76
    logo_size = 48
    gap = 24
    start_x = 32
    start_y = 104
    row_pitch = 126  # distance between category tops
    
    for cat_idx, cat in enumerate(CATEGORIES):
        cat_y = start_y + cat_idx * row_pitch
        cat_name = cat["name"]
        color = cat["color"]
        
        lines.append(f'  <!-- Category: {cat_name} -->')
        lines.append(f'  <g id="cat-{cat["id"]}">' )
        
        # Category Heading: Small & Technical
        lines.append(f'    <text x="{start_x}" y="{cat_y + 14}" fill="{color}" font-family="ui-monospace, monospace" font-size="11" font-weight="700">[{cat["id"]}] {html.escape(cat_name)}</text>')
        lines.append(f'    <line x1="{start_x + 190}" y1="{cat_y + 10}" x2="{W - 32}" y2="{cat_y + 10}" stroke="#1F242C" stroke-width="1"/>')
        
        # Grid of Large Logo Containers
        grid_y = cat_y + 26
        for item_idx, item in enumerate(cat["items"]):
            ix = start_x + item_idx * (box_size + gap)
            iy = grid_y
            
            svg_file = ICONS_DIR / f"{item['key']}.svg"
            if not svg_file.exists():
                print(f"Warning: Missing icon {svg_file}")
                continue
                
            viewBox, inner_xml = sanitize_icon_xml(svg_file, f"{cat['id']}_{item['key']}")
            
            # Icon Container Group
            lines.append(f'    <g class="icon-container" role="img" aria-label="{html.escape(item["name"])}">')
            lines.append(f'      <title>{html.escape(item["name"])}</title>')
            
            # Grey Square Container (#252B33, subtle #343B45 border, rx=10)
            lines.append(f'      <rect class="box-bg" x="{ix}" y="{iy}" width="{box_size}" height="{box_size}" rx="10"/>')
            
            # Centered Large Technology Logo (48x48px)
            lx = ix + (box_size - logo_size) / 2
            ly = iy + (box_size - logo_size) / 2
            lines.append(f'      <svg class="logo-svg" x="{lx:.1f}" y="{ly:.1f}" width="{logo_size}" height="{logo_size}" viewBox="{viewBox}">')
            lines.append(inner_xml)
            lines.append('      </svg>')
            
            # Minimal Hover Tooltip (Only technology name)
            tip_w = max(56, len(item["name"]) * 8 + 16)
            tip_h = 24
            tip_x = ix + (box_size - tip_w) / 2
            tip_y = iy - tip_h - 6
            lines.append('      <g class="tooltip">')
            lines.append(f'        <rect x="{tip_x:.1f}" y="{tip_y:.1f}" width="{tip_w}" height="{tip_h}" rx="4" fill="#161B22" stroke="#484F58" stroke-width="1" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.6))"/>')
            lines.append(f'        <text x="{tip_x + tip_w/2:.1f}" y="{tip_y + 16:.1f}" text-anchor="middle" fill="#F0F6FC" font-family="ui-monospace, monospace" font-size="10" font-weight="600">{html.escape(item["name"])}</text>')
            lines.append('      </g>')
            
            lines.append('    </g>')
            
        lines.append('  </g>')
        
    lines.append('</svg>')
    
    svg_content = "\n".join(lines)
    OUTPUT_FILE.write_text(svg_content, encoding='utf-8')
    print(f"Generated {OUTPUT_FILE} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    render_toolbox()
