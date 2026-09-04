"""Renders system-architecture.svg for Zaid's visual-first developer portfolio."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "system-architecture.svg"


def generate_svg() -> str:
    width, height = 940, 480
    cx = width / 2

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">
  <defs>
    <linearGradient id="flow-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#58A6FF" />
      <stop offset="100%" stop-color="#39D353" />
    </linearGradient>
    <style>
      .bg {{ fill: #080B10; stroke: #30363D; stroke-width: 1; rx: 8px; }}
      .node-card {{ fill: #111820; stroke: #30363D; stroke-width: 1; rx: 6px; transition: all 0.3s; }}
      .node-card:hover {{ stroke: #58A6FF; fill: #161B22; }}
      .node-title {{ fill: #E6EDF3; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 12px; font-weight: 700; }}
      .node-tech {{ fill: #8B949E; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-size: 10.5px; }}
      .flow-line {{ stroke: #58A6FF; stroke-width: 1.5; stroke-dasharray: 6, 6; animation: dash 20s linear infinite; }}
      .branch-line {{ stroke: #39D353; stroke-width: 1.5; stroke-dasharray: 6, 6; animation: dash 20s linear infinite; }}
      .status-live {{ fill: #39D353; }}
      @keyframes dash {{
        to {{ stroke-dashoffset: -1000; }}
      }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" class="bg" />

  <!-- Title Header Bar -->
  <rect x="0" y="0" width="{width}" height="34" fill="#0D1117" rx="8" stroke="#30363D" stroke-width="1" />
  <circle cx="20" cy="17" r="4" fill="#FF5F56" />
  <circle cx="34" cy="17" r="4" fill="#FFBD2E" />
  <circle cx="48" cy="17" r="4" fill="#27C93F" />
  <text x="70" y="21" fill="#8B949E" font-family="ui-monospace, monospace" font-size="11px">~/ 05. system-architecture // PRODUCTION DATA FLOW</text>
  <text x="{width - 24}" y="21" fill="#39D353" font-family="ui-monospace, monospace" font-size="11px" text-anchor="end">SYSTEM HEALTH: 100% ●</text>

  <!-- Connector Lines -->
  <!-- 1. User to Frontend -->
  <line x1="{cx}" y1="88" x2="{cx}" y2="115" class="flow-line" />
  <!-- 2. Frontend to Backend -->
  <line x1="{cx}" y1="167" x2="{cx}" y2="195" class="flow-line" />
  <!-- 3. Backend to DB and Cache branches -->
  <line x1="{cx - 80}" y1="247" x2="{cx - 150}" y2="280" class="branch-line" />
  <line x1="{cx + 80}" y1="247" x2="{cx + 150}" y2="280" class="branch-line" />
  <!-- 4. DB and Cache to Infra -->
  <line x1="{cx - 150}" y1="332" x2="{cx - 80}" y2="365" class="branch-line" />
  <line x1="{cx + 150}" y1="332" x2="{cx + 80}" y2="365" class="branch-line" />
  <!-- 5. Infra to Monitoring -->
  <line x1="{cx}" y1="417" x2="{cx}" y2="435" class="flow-line" />

  <!-- 1. USER NODE -->
  <g transform="translate({cx - 110}, 48)">
    <rect width="220" height="40" class="node-card" stroke="#58A6FF" />
    <circle cx="16" cy="20" r="4" class="status-live" />
    <text x="32" y="24" font-size="14">👥</text>
    <text x="56" y="24" class="node-title">CLIENT / USER</text>
    <text x="180" y="24" fill="#58A6FF" font-family="ui-monospace, monospace" font-size="9px">TLS 1.3</text>
  </g>

  <!-- 2. FRONTEND NODE -->
  <g transform="translate({cx - 170}, 115)">
    <rect width="340" height="52" class="node-card" />
    <circle cx="18" cy="26" r="4" class="status-live" />
    <text x="34" y="32" font-size="18">🌐</text>
    <text x="64" y="24" class="node-title">01. FRONTEND LAYER (SSR / SPA)</text>
    <text x="64" y="42" class="node-tech">React · Next.js · TypeScript · Tailwind CSS · State Cache</text>
  </g>

  <!-- 3. API & BACKEND NODE -->
  <g transform="translate({cx - 180}, 195)">
    <rect width="360" height="52" class="node-card" />
    <circle cx="18" cy="26" r="4" class="status-live" />
    <text x="34" y="32" font-size="18">⚙️</text>
    <text x="64" y="24" class="node-title">02. API &amp; BACKEND SERVICES</text>
    <text x="64" y="42" class="node-tech">Node.js · FastAPI · Go · REST / GraphQL · JWT Security</text>
  </g>

  <!-- 4A. PRIMARY DATABASE (Left Branch) -->
  <g transform="translate({cx - 320}, 280)">
    <rect width="260" height="52" class="node-card" />
    <circle cx="16" cy="26" r="4" class="status-live" />
    <text x="30" y="32" font-size="16">🗄️</text>
    <text x="56" y="24" class="node-title">03A. PRIMARY STORAGE</text>
    <text x="56" y="42" class="node-tech">PostgreSQL · MongoDB · Prisma</text>
  </g>

  <!-- 4B. CACHE & IN-MEMORY (Right Branch) -->
  <g transform="translate({cx + 60}, 280)">
    <rect width="260" height="52" class="node-card" />
    <circle cx="16" cy="26" r="4" class="status-live" />
    <text x="30" y="32" font-size="16">⚡</text>
    <text x="56" y="24" class="node-title">03B. IN-MEMORY CACHE</text>
    <text x="56" y="42" class="node-tech">Redis (Pub/Sub, Rate Limits, TTL)</text>
  </g>

  <!-- 5. INFRASTRUCTURE NODE -->
  <g transform="translate({cx - 180}, 365)">
    <rect width="360" height="52" class="node-card" />
    <circle cx="18" cy="26" r="4" class="status-live" />
    <text x="34" y="32" font-size="18">☁️</text>
    <text x="64" y="24" class="node-title">04. CLOUD INFRASTRUCTURE &amp; CI/CD</text>
    <text x="64" y="42" class="node-tech">Docker Containers · GitHub Actions CI · Cloud Linux</text>
  </g>

  <!-- 6. MONITORING NODE -->
  <g transform="translate({cx - 140}, 435)">
    <rect width="280" height="34" class="node-card" stroke="#39D353" />
    <circle cx="16" cy="17" r="4" class="status-live" />
    <text x="28" y="23" font-size="14">📊</text>
    <text x="50" y="21" class="node-title">05. TELEMETRY &amp; AUDITS</text>
    <text x="200" y="21" fill="#39D353" font-family="ui-monospace, monospace" font-size="9px">[ACTIVE 24/7]</text>
  </g>
</svg>"""


def main():
    svg = generate_svg()
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"[OK] Generated {OUTPUT.name} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
