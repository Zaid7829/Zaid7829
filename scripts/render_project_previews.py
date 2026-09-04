"""Renders visual UI preview mockups (project-devos.svg and project-staging.svg) for Zaid's projects."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEVOS_OUTPUT = ROOT / "project-devos.svg"
STAGING_OUTPUT = ROOT / "project-staging.svg"


def generate_devos_svg() -> str:
    w, h = 540, 240
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  <defs>
    <style>
      .window-bg {{ fill: #0D1117; stroke: #30363D; stroke-width: 1; rx: 8px; }}
      .title-bar {{ fill: #161B22; }}
      .title-text {{ fill: #8B949E; font-family: ui-monospace, monospace; font-size: 11px; }}
      .code-line {{ font-family: ui-monospace, monospace; font-size: 11px; }}
      .kw {{ fill: #FF7B72; }}
      .fn {{ fill: #D2A8FF; }}
      .str {{ fill: #A5D6FF; }}
      .comment {{ fill: #8B949E; }}
      .accent-box {{ fill: #111820; stroke: #58A6FF; stroke-width: 1; rx: 6px; }}
    </style>
  </defs>

  <rect width="{w}" height="{h}" class="window-bg" />
  <rect width="{w}" height="28" class="title-bar" rx="8" />
  <circle cx="16" cy="14" r="4" fill="#FF5F56" />
  <circle cx="28" cy="14" r="4" fill="#FFBD2E" />
  <circle cx="40" cy="14" r="4" fill="#27C93F" />
  <text x="60" y="18" class="title-text">engine.py — Zaid7829/Zaid7829 [Active Profile OS]</text>

  <!-- Code Snippet Area -->
  <g transform="translate(20, 48)">
    <text y="14" class="code-line"><tspan class="kw">class</tspan> <tspan class="fn">DeveloperOS</tspan>:</text>
    <text y="34" class="code-line">  <tspan class="kw">def</tspan> <tspan class="fn">build_runtime</tspan>(self):</text>
    <text y="54" class="code-line">    self.stack = [<tspan class="str">"React"</tspan>, <tspan class="str">"TypeScript"</tspan>, <tspan class="str">"FastAPI"</tspan>, <tspan class="str">"Docker"</tspan>]</text>
    <text y="74" class="code-line">    self.pipeline.deploy(zero_downtime=<tspan class="kw">True</tspan>)</text>
    <text y="94" class="code-line">    <tspan class="comment"># Telemetry: 100% automated vector SVG builds</tspan></text>
  </g>

  <!-- Right Visual Widget: Mini Dot Matrix -->
  <g transform="translate(340, 45)">
    <rect width="180" height="175" class="accent-box" />
    <text x="90" y="24" fill="#58A6FF" font-family="ui-monospace, monospace" font-size="10px" text-anchor="middle" font-weight="bold">SYSTEM TELEMETRY</text>
    <circle cx="90" cy="75" r="32" fill="none" stroke="#39D353" stroke-width="3" stroke-dasharray="140, 20" />
    <text x="90" y="80" fill="#E6EDF3" font-family="ui-monospace, monospace" font-size="12px" text-anchor="middle" font-weight="bold">HEALTH</text>
    <text x="90" y="130" fill="#8B949E" font-family="ui-monospace, monospace" font-size="10px" text-anchor="middle">UPTIME: 99.99%</text>
    <text x="90" y="148" fill="#39D353" font-family="ui-monospace, monospace" font-size="10px" text-anchor="middle">ACTIVE CRON SYNC</text>
  </g>
</svg>"""


def generate_staging_svg() -> str:
    w, h = 540, 240
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}">
  <defs>
    <style>
      .window-bg {{ fill: #0D1117; stroke: #30363D; stroke-width: 1; rx: 8px; }}
      .title-bar {{ fill: #161B22; }}
      .title-text {{ fill: #8B949E; font-family: ui-monospace, monospace; font-size: 11px; }}
      .dash-card {{ fill: #111820; stroke: #30363D; stroke-width: 1; rx: 6px; }}
      .metric-val {{ fill: #E6EDF3; font-family: ui-monospace, monospace; font-size: 16px; font-weight: bold; }}
      .metric-lbl {{ fill: #8B949E; font-family: ui-monospace, monospace; font-size: 9.5px; }}
    </style>
  </defs>

  <rect width="{w}" height="{h}" class="window-bg" />
  <rect width="{w}" height="28" class="title-bar" rx="8" />
  <circle cx="16" cy="14" r="4" fill="#FF5F56" />
  <circle cx="28" cy="14" r="4" fill="#FFBD2E" />
  <circle cx="40" cy="14" r="4" fill="#27C93F" />
  <text x="60" y="18" class="title-text">cluster-dashboard — Full-Stack Staging Environment</text>

  <!-- Metric 1: API Throughput -->
  <g transform="translate(20, 45)">
    <rect width="155" height="80" class="dash-card" stroke="#58A6FF" />
    <text x="14" y="24" class="metric-lbl">API LATENCY (p99)</text>
    <text x="14" y="52" class="metric-val" fill="#58A6FF">24 ms</text>
    <text x="14" y="70" fill="#39D353" font-family="ui-monospace, monospace" font-size="9px">● NOMINAL</text>
  </g>

  <!-- Metric 2: DB Connection Pool -->
  <g transform="translate(190, 45)">
    <rect width="155" height="80" class="dash-card" stroke="#39D353" />
    <text x="14" y="24" class="metric-lbl">DB CONNECTIONS</text>
    <text x="14" y="52" class="metric-val">12 / 100</text>
    <text x="14" y="70" fill="#39D353" font-family="ui-monospace, monospace" font-size="9px">● POOL STABLE</text>
  </g>

  <!-- Metric 3: Cache Hit Ratio -->
  <g transform="translate(360, 45)">
    <rect width="160" height="80" class="dash-card" stroke="#FF8C00" />
    <text x="14" y="24" class="metric-lbl">REDIS CACHE HIT</text>
    <text x="14" y="52" class="metric-val">98.4%</text>
    <text x="14" y="70" fill="#FF8C00" font-family="ui-monospace, monospace" font-size="9px">● LOW LATENCY</text>
  </g>

  <!-- Lower Terminal Status Area -->
  <g transform="translate(20, 140)">
    <rect width="500" height="80" class="dash-card" />
    <text x="16" y="24" fill="#8B949E" font-family="ui-monospace, monospace" font-size="10px">$ docker compose -f docker-compose.prod.yml up --build -d</text>
    <text x="16" y="44" fill="#39D353" font-family="ui-monospace, monospace" font-size="10px">[+] Running 4/4: Container web [Started] · Container api [Started] · Redis [Started]</text>
    <text x="16" y="64" fill="#58A6FF" font-family="ui-monospace, monospace" font-size="10px">[✓] All contracts validated: Zero regressions detected</text>
  </g>
</svg>"""


def main():
    devos_svg = generate_devos_svg()
    DEVOS_OUTPUT.write_text(devos_svg, encoding="utf-8")
    print(f"[OK] Generated {DEVOS_OUTPUT.name} ({len(devos_svg)} bytes)")

    staging_svg = generate_staging_svg()
    STAGING_OUTPUT.write_text(staging_svg, encoding="utf-8")
    print(f"[OK] Generated {STAGING_OUTPUT.name} ({len(staging_svg)} bytes)")


if __name__ == "__main__":
    main()
