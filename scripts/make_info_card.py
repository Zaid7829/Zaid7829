#!/usr/bin/env python3
"""
Generate a compact, personal, memorable terminal identity card for Zaid.
Specifications:
- Section: ~/ 01. whoami
- Communicates: AI Engineer · Full Stack Developer · Software Engineer · Problem Solver / Builder
- Personal & authentic developer voice (zero corporate resume buzzwords)
- Current Builds: Aura & AgentFlow with direct clickable links
- Developer workflow: CODE → EXPERIMENT → BREAK → DEBUG → BUILD AGAIN
- Compact size: 760x300 (drastically shorter than previous 760x760)
- Terminal aesthetic: window controls, command prompt, dark mode theme
- Output: info-card.svg
"""
from __future__ import annotations
import html
from pathlib import Path

OUTPUT_PATH = Path("info-card.svg")

W, H = 760, 304

def esc(text: str) -> str:
    return html.escape(str(text), quote=True)

def generate_card():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Zaid — Identity Card">')
    lines.append('  <title>Zaid — Identity Card</title>')
    lines.append('  <desc>AI Engineer, Full Stack Developer, and Builder — Personal identity and current builds</desc>')
    
    # CSS Styles & Interactive Transitions
    lines.append('  <style>')
    lines.append('    .mono { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Monaco, Consolas, monospace; }')
    lines.append('    .term-link {')
    lines.append('      cursor: pointer;')
    lines.append('      text-decoration: none;')
    lines.append('    }')
    lines.append('    .term-link .card-btn {')
    lines.append('      fill: #161B22;')
    lines.append('      stroke: #30363D;')
    lines.append('      stroke-width: 1px;')
    lines.append('      transition: fill 0.2s ease, stroke 0.2s ease;')
    lines.append('    }')
    lines.append('    .term-link:hover .card-btn {')
    lines.append('      fill: #21262D;')
    lines.append('      stroke: #58A6FF;')
    lines.append('    }')
    lines.append('    .term-link:hover .btn-text {')
    lines.append('      fill: #58A6FF;')
    lines.append('    }')
    lines.append('    .cursor {')
    lines.append('      animation: termBlink 0.8s step-end infinite;')
    lines.append('    }')
    lines.append('    @keyframes termBlink {')
    lines.append('      0%, 100% { opacity: 1; }')
    lines.append('      50% { opacity: 0; }')
    lines.append('    }')
    lines.append('  </style>')
    
    # Gradients
    lines.append('  <defs>')
    lines.append('    <radialGradient id="card-bg" cx="50%" cy="30%" r="80%">')
    lines.append('      <stop offset="0%" stop-color="#111620"/>')
    lines.append('      <stop offset="60%" stop-color="#0A0E14"/>')
    lines.append('      <stop offset="100%" stop-color="#06080B"/>')
    lines.append('    </radialGradient>')
    lines.append('  </defs>')
    
    # Outer Terminal Frame
    lines.append(f'  <rect width="{W}" height="{H}" rx="14" fill="url(#card-bg)"/>')
    lines.append(f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13" fill="none" stroke="#30363D" stroke-width="1.2"/>')
    
    # Terminal Title Bar
    lines.append(f'  <rect x="1" y="1" width="{W-2}" height="38" rx="13" fill="#0D1117"/>')
    lines.append(f'  <line x1="1" y1="39" x2="{W-1}" y2="39" stroke="#21262D" stroke-width="1"/>')
    lines.append('  <circle cx="20" cy="20" r="5" fill="#FF5F56"/>')
    lines.append('  <circle cx="36" cy="20" r="5" fill="#FFBD2E"/>')
    lines.append('  <circle cx="52" cy="20" r="5" fill="#27C93F"/>')
    lines.append('  <text class="mono" x="74" y="24" fill="#8B949E" font-size="12">zaid@github:~$ whoami</text>')
    lines.append(f'  <text class="mono" x="{W-24}" y="24" text-anchor="end" fill="#39D353" font-size="11">● ACTIVE // BUILDER</text>')
    
    # Header: Name & Core Identity
    lines.append('  <!-- Header: Identity -->')
    lines.append('  <text class="mono" x="32" y="68" fill="#FF8C00" font-size="18" font-weight="700">ZAID</text>')
    lines.append('  <text class="mono" x="88" y="68" fill="#30363D" font-size="14">│</text>')
    lines.append('  <text class="mono" x="104" y="67" fill="#58A6FF" font-size="11.5" font-weight="600" letter-spacing="0.08em">AI ENGINEER  ·  FULL STACK DEVELOPER  ·  SOFTWARE ENGINEER</text>')
    lines.append(f'  <line x1="32" y1="80" x2="{W-32}" y2="80" stroke="#21262D" stroke-width="1"/>')
    
    # Natural Developer Statement (3 clean lines)
    lines.append('  <!-- Bio Statement -->')
    lines.append('  <text class="mono" x="32" y="106" fill="#C9D1D9" font-size="12.5">')
    lines.append('    <tspan fill="#E6EDF3" font-weight="600">I’m Zaid</tspan> — an engineer who genuinely enjoys <tspan fill="#F0F6FC">building things</tspan> and solving complex problems.')
    lines.append('  </text>')
    lines.append('  <text class="mono" x="32" y="128" fill="#C9D1D9" font-size="12.5">')
    lines.append('    I like taking an idea, figuring out how it should work, and turning it into software that actually works.')
    lines.append('  </text>')
    lines.append('  <text class="mono" x="32" y="150" fill="#8B949E" font-size="12">')
    lines.append('    Most learning happens by building, breaking, debugging, and following useful rabbit holes.')
    lines.append('  </text>')
    
    # Divider line
    lines.append(f'  <line x1="32" y1="168" x2="{W-32}" y2="168" stroke="#1F242C" stroke-width="1"/>')
    
    # Currently Building Row
    lines.append('  <!-- Currently Building -->')
    lines.append('  <text class="mono" x="32" y="196" fill="#8B949E" font-size="11" font-weight="700">CURRENTLY BUILDING</text>')
    
    # Project 1: Aura
    lines.append('  <a class="term-link" href="https://github.com/Zaid7829/Aura" target="_blank" rel="noopener noreferrer">')
    lines.append('    <rect class="card-btn" x="194" y="179" width="138" height="28" rx="6"/>')
    # Octocat / diamond icon
    lines.append('    <circle cx="210" cy="193" r="4.5" fill="#58A6FF"/>')
    lines.append('    <text class="mono btn-text" x="222" y="197" fill="#E6EDF3" font-size="11.5" font-weight="600">Aura</text>')
    lines.append('    <text class="mono" x="316" y="197" fill="#8B949E" font-size="11">↗</text>')
    lines.append('  </a>')
    
    # Project 2: AgentFlow
    lines.append('  <a class="term-link" href="https://github.com/Zaid7829/AgentFlow" target="_blank" rel="noopener noreferrer">')
    lines.append('    <rect class="card-btn" x="344" y="179" width="168" height="28" rx="6"/>')
    lines.append('    <circle cx="360" cy="193" r="4.5" fill="#39D353"/>')
    lines.append('    <text class="mono btn-text" x="372" y="197" fill="#E6EDF3" font-size="11.5" font-weight="600">AgentFlow</text>')
    lines.append('    <text class="mono" x="496" y="197" fill="#8B949E" font-size="11">↗</text>')
    lines.append('  </a>')
    
    # Developer Workflow Pipeline
    lines.append('  <!-- Developer Workflow Pipeline -->')
    lines.append(f'  <rect x="32" y="224" width="{W-64}" height="48" rx="8" fill="#0D1117" stroke="#21262D" stroke-width="1"/>')
    
    lines.append('  <text class="mono" x="48" y="253" font-size="11.5">')
    lines.append('    <tspan fill="#8B949E" font-weight="700">WORKFLOW: </tspan>')
    lines.append('    <tspan fill="#58A6FF" font-weight="600">CODE</tspan>')
    lines.append('    <tspan fill="#484F58"> → </tspan>')
    lines.append('    <tspan fill="#A371F7" font-weight="600">EXPERIMENT</tspan>')
    lines.append('    <tspan fill="#484F58"> → </tspan>')
    lines.append('    <tspan fill="#F85149" font-weight="600">BREAK</tspan>')
    lines.append('    <tspan fill="#484F58"> → </tspan>')
    lines.append('    <tspan fill="#FF8C00" font-weight="600">DEBUG</tspan>')
    lines.append('    <tspan fill="#484F58"> → </tspan>')
    lines.append('    <tspan fill="#39D353" font-weight="600">BUILD AGAIN</tspan>')
    lines.append('    <tspan class="cursor" fill="#39D353">_</tspan>')
    lines.append('  </text>')
    
    lines.append('</svg>')
    
    content = "\n".join(lines)
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Generated {OUTPUT_PATH} ({len(content)} bytes)")

if __name__ == "__main__":
    generate_card()
