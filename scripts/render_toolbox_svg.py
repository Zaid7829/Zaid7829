#!/usr/bin/env python3
"""
Generate a self-contained, unified dark terminal toolbox SVG.
Output: toolbox.svg (940x580)
"""
from __future__ import annotations
import html
import json
from pathlib import Path

OUTPUT_FILE = Path("toolbox.svg")

CATEGORIES = [
    {
        "id": "01",
        "name": "LANGUAGES",
        "color": "#FF8C00",
        "items": ["TypeScript", "JavaScript", "Python", "Java", "C", "C++", "Go", "Rust", "PHP", "SQL", "Bash"]
    },
    {
        "id": "02",
        "name": "FRONTEND",
        "color": "#FFD166",
        "items": ["React", "Next.js", "Vue", "Angular", "Svelte", "Tailwind CSS", "Redux", "Vite", "HTML5", "CSS3"]
    },
    {
        "id": "03",
        "name": "BACKEND & APIS",
        "color": "#58A6FF",
        "items": ["Node.js", "Express", "NestJS", "FastAPI", "Django", "Flask", "Spring Boot", ".NET", "REST", "GraphQL", "WebSockets"]
    },
    {
        "id": "04",
        "name": "DATABASES",
        "color": "#39D353",
        "items": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Prisma", "Drizzle", "SQLAlchemy"]
    },
    {
        "id": "05",
        "name": "CLOUD & DEVOPS",
        "color": "#79C0FF",
        "items": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform", "Vercel", "Nginx", "Linux", "CI/CD"]
    },
    {
        "id": "06",
        "name": "TESTING & QA",
        "color": "#FF7B72",
        "items": ["Jest", "Vitest", "Pytest", "Playwright", "Cypress", "Testing Library"]
    },
    {
        "id": "07",
        "name": "AI & MACHINE LEARNING",
        "color": "#D2A8FF",
        "items": ["OpenAI", "LLM Apps", "LangChain", "Hugging Face", "scikit-learn", "PyTorch", "TensorFlow"]
    },
    {
        "id": "08",
        "name": "TOOLS & WORKFLOW",
        "color": "#56D364",
        "items": ["Git", "GitHub Actions", "VS Code", "Postman", "Figma", "Linux CLI"]
    }
]

W, H = 940, 580

def esc(text: str) -> str:
    return html.escape(str(text), quote=True)

def render_toolbox():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Zaid7829 developer toolbox and technology radar">')
    lines.append('  <title>Zaid7829 — Developer Toolbox</title>')
    lines.append('  <desc>Categorized technology radar displaying languages, frameworks, cloud, databases, and tooling</desc>')
    
    # Outer Terminal Frame
    lines.append(f'  <rect width="{W}" height="{H}" rx="16" fill="#080B10"/>')
    lines.append(f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="#30363D" stroke-width="1.2"/>')
    
    # Terminal Title Bar
    lines.append(f'  <rect x="1" y="1" width="{W-2}" height="40" rx="15" fill="#0D1117"/>')
    lines.append(f'  <line x1="1" y1="41" x2="{W-1}" y2="41" stroke="#21262D" stroke-width="1"/>')
    lines.append('  <circle cx="22" cy="21" r="5" fill="#FF5F56"/>')
    lines.append('  <circle cx="38" cy="21" r="5" fill="#FFBD2E"/>')
    lines.append('  <circle cx="54" cy="21" r="5" fill="#27C93F"/>')
    lines.append('  <text x="76" y="25" fill="#8B949E" font-family="monospace" font-size="12">zaid@github:~$ ./toolbox --ecosystem --grid</text>')
    lines.append(f'  <text x="{W-24}" y="25" text-anchor="end" fill="#FF8C00" font-family="monospace" font-size="11">TECH_RADAR // ACTIVE_INVENTORY</text>')
    
    # Section Header
    lines.append('  <text x="32" y="70" fill="#FF8C00" font-family="monospace" font-size="14" font-weight="700">~/ toolbox</text>')
    lines.append('  <text x="130" y="70" fill="#8B949E" font-family="monospace" font-size="11">Technology ecosystem — tools and frameworks evaluated, explored, and shipped</text>')
    lines.append(f'  <line x1="32" y1="82" x2="{W-32}" y2="82" stroke="#21262D" stroke-width="1"/>')
    
    # Layout 8 categories in a 2-column x 4-row grid
    # Left column: categories 0, 1, 2, 3
    # Right column: categories 4, 5, 6, 7
    col_w = 426
    start_y = 100
    row_height = 105
    
    for i, cat in enumerate(CATEGORIES):
        is_right = (i >= 4)
        row_idx = i if not is_right else (i - 4)
        
        col_x = 32 if not is_right else (32 + col_w + 24)
        cat_y = start_y + row_idx * row_height
        
        # Category Panel Background
        lines.append(f'  <!-- Category: {esc(cat["name"])} -->')
        lines.append(f'  <rect x="{col_x}" y="{cat_y}" width="{col_w}" height="95" rx="8" fill="#0D1117" stroke="#21262D" stroke-width="1"/>')
        
        # Category Header
        lines.append(f'  <circle cx="{col_x+16}" cy="{cat_y+16}" r="3.5" fill="{cat["color"]}"/>')
        lines.append(f'  <text x="{col_x+28}" y="{cat_y+19}" fill="{cat["color"]}" font-family="monospace" font-size="10.5" font-weight="700">[{cat["id"]}] {esc(cat["name"])}</text>')
        
        # Chips container
        chip_x = col_x + 14
        chip_y = cat_y + 34
        max_row_x = col_x + col_w - 14
        
        cur_x = chip_x
        cur_y = chip_y
        
        for item in cat["items"]:
            # calculate approx chip width based on character count
            # padding 14 + chars * 7.2
            cw = int(18 + len(item) * 7.0)
            if cur_x + cw > max_row_x:
                cur_x = chip_x
                cur_y += 26
                
            lines.append(f'  <rect x="{cur_x}" y="{cur_y}" width="{cw}" height="20" rx="4" fill="#111820" stroke="#30363D" stroke-width="0.8"/>')
            lines.append(f'  <circle cx="{cur_x+8}" cy="{cur_y+10}" r="2" fill="{cat["color"]}" opacity="0.85"/>')
            lines.append(f'  <text x="{cur_x+15}" y="{cur_y+14}" fill="#E6EDF3" font-family="monospace" font-size="9.5">{esc(item)}</text>')
            cur_x += cw + 6
            
    # Bottom Footer
    lines.append(f'  <!-- Terminal Footer -->')
    lines.append(f'  <line x1="24" y1="{H-40}" x2="{W-24}" y2="{H-40}" stroke="#21262D" stroke-width="1"/>')
    lines.append(f'  <circle cx="34" cy="{H-20}" r="4" fill="#FF8C00"/>')
    lines.append(f'  <text x="46" y="{H-17}" fill="#8B949E" font-family="monospace" font-size="10.5">RADAR NOTE: Active development &amp; exploration index · not a claim of universal mastery</text>')
    lines.append(f'  <text x="{W-24}" y="{H-17}" text-anchor="end" fill="#6E7681" font-family="monospace" font-size="10.5">56 TECHNOLOGIES // 8 DOMAINS</text>')
    
    lines.append('</svg>')
    
    svg_content = "\n".join(lines)
    OUTPUT_FILE.write_text(svg_content, encoding="utf-8")
    print(f"Rendered {OUTPUT_FILE} ({len(svg_content.encode('utf-8')) / 1024:.1f} KB)")

if __name__ == "__main__":
    render_toolbox()
