#!/usr/bin/env python3
"""
Generate a compact terminal session footer SVG for Zaid's profile.
Output: terminal-footer.svg (760x180)
"""
from __future__ import annotations
import html
from pathlib import Path

OUTPUT_FILE = Path("terminal-footer.svg")
W, H = 760, 170

def esc(text: str) -> str:
    return html.escape(str(text), quote=True)

def render_footer_svg():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal Session Completed">')
    lines.append('  <title>zaid@github:~$ exit</title>')
    lines.append('  <desc>Terminal session closed: Build something useful. Learn something new. Ship something better.</desc>')
    
    # Fonts and styles
    lines.append('  <style>')
    lines.append('    .mono { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; }')
    lines.append('    .subtle-pulse {')
    lines.append('      animation: statusPulse 4s ease-in-out infinite;')
    lines.append('    }')
    lines.append('    @keyframes statusPulse {')
    lines.append('      0%, 100% { opacity: 0.6; }')
    lines.append('      50% { opacity: 0.9; }')
    lines.append('    }')
    lines.append('    @media (prefers-reduced-motion: reduce) {')
    lines.append('      .subtle-pulse { animation: none; opacity: 0.7; }')
    lines.append('    }')
    lines.append('  </style>')
    
    # Outer Terminal Box
    lines.append(f'  <rect width="{W}" height="{H}" rx="6" fill="#0D1117" stroke="#30363D" stroke-width="1"/>')
    
    # Terminal Title Bar
    lines.append(f'  <path d="M 0 6 A 6 6 0 0 1 6 0 L {W-6} 0 A 6 6 0 0 1 {W} 6 L {W} 34 L 0 34 Z" fill="#161B22" />')
    lines.append(f'  <line x1="0" y1="34" x2="{W}" y2="34" stroke="#30363D" stroke-width="1"/>')
    
    # Muted window dots (terminal session completed)
    lines.append('  <circle cx="18" cy="17" r="4.5" fill="#484F58" />')
    lines.append('  <circle cx="32" cy="17" r="4.5" fill="#484F58" />')
    lines.append('  <circle cx="46" cy="17" r="4.5" fill="#484F58" />')
    
    # Terminal command in titlebar
    lines.append('  <text x="64" y="21" class="mono" fill="#8B949E" font-size="12">zaid@github:~$ exit</text>')
    
    # Understated status indicator: ● SESSION CLOSED
    lines.append(f'  <g class="subtle-pulse">')
    lines.append(f'    <text x="{W-18}" y="21" text-anchor="end" class="mono" fill="#8B949E" font-size="11">● SESSION CLOSED</text>')
    lines.append(f'  </g>')
    
    # Body: [ PROCESS COMPLETED ]
    lines.append('  <text x="24" y="60" class="mono" fill="#58A6FF" font-size="13" font-weight="600">[ PROCESS COMPLETED ]</text>')
    
    # Terminal closing lines
    lines.append('  <text x="24" y="86" class="mono" fill="#C9D1D9" font-size="12">Build something useful.</text>')
    lines.append('  <text x="24" y="106" class="mono" fill="#C9D1D9" font-size="12">Learn something new.</text>')
    lines.append('  <text x="24" y="126" class="mono" fill="#C9D1D9" font-size="12">Ship something better.</text>')
    
    # Bottom divider line
    lines.append(f'  <line x1="24" y1="142" x2="{W-24}" y2="142" stroke="#21262D" stroke-width="1"/>')
    
    # Bottom copyright & system attribution
    lines.append(f'  <text x="24" y="157" class="mono" fill="#6E7681" font-size="11">© Zaid · Developer Operating System · 2026</text>')
    lines.append(f'  <text x="{W-24}" y="157" text-anchor="end" class="mono" fill="#484F58" font-size="11">DEV_OS v2.6 // TTY1</text>')
    
    lines.append('</svg>')
    
    content = "\n".join(lines) + "\n"
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(f"[OK] Generated {OUTPUT_FILE} ({len(content)} bytes)")

if __name__ == "__main__":
    render_footer_svg()
