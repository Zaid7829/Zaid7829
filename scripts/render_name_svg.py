#!/usr/bin/env python3
"""
Generate an animated typewriter SVG for Zaid's GitHub profile header.
Specifications:
- Text: "Z  A  I  D" (clean, elegant, bold tracking)
- True slow typewriter effect: deliberate, slow mechanical cadence with relaxed blinking cursor
- Color cycle: Types out in a different vibrant accent color every cycle:
    1. Electric Cyan    (#38BDF8)
    2. Terminal Green   (#39D353)
    3. Cyberpunk Violet (#A371F7)
    4. Sunset Amber     (#FF8C00)
    5. Neon Rose        (#F43F5E)
    6. Platinum White   (#F0F6FC)
- Fixed start coordinate: Text does NOT shift/jitter while typing; types naturally from left to right.
- Perfectly centered when full name is typed.
- Self-contained SVG, zero external dependencies, 100% GitHub camo & dark-mode compatible.
- Size: 600x64 (viewBox: 0 0 600 64)
"""

from pathlib import Path

OUTPUT_FILE = Path("hero-name.svg")

COLORS = [
    ("#38BDF8", "Electric Cyan"),
    ("#39D353", "Terminal Green"),
    ("#A371F7", "Cyberpunk Violet"),
    ("#FF8C00", "Sunset Amber"),
    ("#F43F5E", "Neon Rose"),
    ("#F0F6FC", "Platinum White")
]

# Total animation duration: 48s (8.0s per color cycle * 6 colors)
# Slow, relaxed, deliberate typing cadence
CYCLE_DURATION = 8.0  # seconds per color
NUM_CYCLES = len(COLORS)
TOTAL_DURATION = CYCLE_DURATION * NUM_CYCLES  # 48.0s

# Within each 8.0s cycle:
# 0.00s - 0.80s (0.00% - 10.00%): Frame 0: "|" (slow initial blink)
# 0.80s - 1.55s (10.00% - 19.38%): Frame 1: "Z |" (slow typing)
# 1.55s - 2.30s (19.38% - 28.75%): Frame 2: "Z  A |" (slow typing)
# 2.30s - 3.05s (28.75% - 38.12%): Frame 3: "Z  A  I |" (slow typing)
# 3.05s - 6.00s (38.12% - 75.00%): Frame 4: "Z  A  I  D |" (hold & admire for ~3 full seconds, cursor blinks slowly)
# 6.00s - 6.45s (75.00% - 80.62%): Frame 3: "Z  A  I |" (backspace)
# 6.45s - 6.90s (80.62% - 86.25%): Frame 2: "Z  A |" (backspace)
# 6.90s - 7.35s (86.25% - 91.88%): Frame 1: "Z |" (backspace)
# 7.35s - 8.00s (91.88% - 100.0%): Frame 0: "|" (pause before next color)

# Monospace metrics (font-size: 34px):
# Total width of "Z  A  I  D" (with double spaces) = ~216px.
# Center of 600px width = 300px.
# Start X = 300 - 108 = 192px.

X_START = 192
Y_POS = 34

def generate_svg():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 64" width="600" height="64" role="img" aria-label="Zaid typewriter name banner">')
    lines.append('  <title>Z A I D</title>')
    lines.append('  <style>')
    lines.append('    .type-text {')
    lines.append('      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Monaco, Consolas, monospace;')
    lines.append('      font-size: 34px;')
    lines.append('      font-weight: 800;')
    lines.append('      letter-spacing: 0.18em;')
    lines.append('      dominant-baseline: central;')
    lines.append('      text-anchor: start;')
    lines.append('    }')
    lines.append('    .cursor {')
    lines.append('      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;')
    lines.append('      font-weight: 300;')
    lines.append('      font-size: 32px;')
    lines.append('      animation: cursorBlink 0.85s step-end infinite;')
    lines.append('    }')
    lines.append('    @keyframes cursorBlink {')
    lines.append('      0%, 100% { opacity: 1; }')
    lines.append('      50% { opacity: 0; }')
    lines.append('    }')
    
    # 1. Cycle color & visibility keyframes (48s loop)
    for i, (color, name) in enumerate(COLORS):
        c_start = (i / NUM_CYCLES) * 100.0
        c_end = ((i + 1) / NUM_CYCLES) * 100.0
        
        lines.append(f'    /* Cycle {i}: {name} ({color}) */')
        lines.append(f'    .cycle-{i} {{')
        lines.append(f'      fill: {color};')
        lines.append(f'      animation: cycleAnim{i} {TOTAL_DURATION}s infinite;')
        lines.append('    }')
        lines.append(f'    @keyframes cycleAnim{i} {{')
        if i == 0:
            lines.append(f'      0%, {c_end - 0.01:.2f}% {{ opacity: 1; visibility: visible; }}')
            lines.append(f'      {c_end:.2f}%, 100% {{ opacity: 0; visibility: hidden; }}')
        elif i == NUM_CYCLES - 1:
            lines.append(f'      0%, {c_start - 0.01:.2f}% {{ opacity: 0; visibility: hidden; }}')
            lines.append(f'      {c_start:.2f}%, 100% {{ opacity: 1; visibility: visible; }}')
        else:
            lines.append(f'      0%, {c_start - 0.01:.2f}% {{ opacity: 0; visibility: hidden; }}')
            lines.append(f'      {c_start:.2f}%, {c_end - 0.01:.2f}% {{ opacity: 1; visibility: visible; }}')
            lines.append(f'      {c_end:.2f}%, 100% {{ opacity: 0; visibility: hidden; }}')
        lines.append('    }')
    
    # 2. Frame cadence keyframes (8.0s loop per cycle) - SLOW TYPEWRITER
    frame_timings = [
        (0, [(0.00, 10.00), (91.88, 100.00)]),
        (1, [(10.00, 19.38), (86.25, 91.88)]),
        (2, [(19.38, 28.75), (80.62, 86.25)]),
        (3, [(28.75, 38.12), (75.00, 80.62)]),
        (4, [(38.12, 75.00)])  # Holds for ~3 full seconds
    ]
    
    for f_idx, intervals in frame_timings:
        lines.append(f'    .frame-{f_idx} {{')
        lines.append(f'      animation: frameAnim{f_idx} {CYCLE_DURATION}s infinite;')
        lines.append('    }')
        lines.append(f'    @keyframes frameAnim{f_idx} {{')
        
        cur = 0.0
        for start, end in intervals:
            if start > cur:
                lines.append(f'      {cur:.2f}%, {start - 0.01:.2f}% {{ opacity: 0; visibility: hidden; }}')
            lines.append(f'      {start:.2f}%, {end - 0.01:.2f}% {{ opacity: 1; visibility: visible; }}')
            cur = end
        if cur < 100.0:
            lines.append(f'      {cur:.2f}%, 100% {{ opacity: 0; visibility: hidden; }}')
            
        lines.append('    }')
        
    lines.append('  </style>')
    
    # SVG Content Groups
    for c_idx, (color, c_name) in enumerate(COLORS):
        lines.append(f'  <!-- Cycle {c_idx}: {c_name} -->')
        lines.append(f'  <g class="cycle-{c_idx}">')
        
        # Frame 0: "|" (cursor only at X_START)
        lines.append(f'    <g class="frame-0">')
        lines.append(f'      <text class="type-text" x="{X_START}" y="{Y_POS}"><tspan class="cursor">|</tspan></text>')
        lines.append('    </g>')
        
        # Frame 1: "Z |"
        lines.append(f'    <g class="frame-1">')
        lines.append(f'      <text class="type-text" x="{X_START}" y="{Y_POS}">Z<tspan class="cursor">&#160;|</tspan></text>')
        lines.append('    </g>')
        
        # Frame 2: "Z  A |"
        lines.append(f'    <g class="frame-2">')
        lines.append(f'      <text class="type-text" x="{X_START}" y="{Y_POS}">Z&#160;&#160;A<tspan class="cursor">&#160;|</tspan></text>')
        lines.append('    </g>')
        
        # Frame 3: "Z  A  I |"
        lines.append(f'    <g class="frame-3">')
        lines.append(f'      <text class="type-text" x="{X_START}" y="{Y_POS}">Z&#160;&#160;A&#160;&#160;I<tspan class="cursor">&#160;|</tspan></text>')
        lines.append('    </g>')
        
        # Frame 4: "Z  A  I  D |"
        lines.append(f'    <g class="frame-4">')
        lines.append(f'      <text class="type-text" x="{X_START}" y="{Y_POS}">Z&#160;&#160;A&#160;&#160;I&#160;&#160;D<tspan class="cursor">&#160;|</tspan></text>')
        lines.append('    </g>')
        
        lines.append('  </g>')
        
    lines.append('</svg>')
    
    content = "\n".join(lines)
    OUTPUT_FILE.write_text(content, encoding='utf-8')
    print(f"Generated {OUTPUT_FILE} ({len(content)} bytes)")

if __name__ == "__main__":
    generate_svg()
