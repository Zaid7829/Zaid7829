"""Local browser preview server for README.md using GitHub's markdown renderer.

Usage:
    python scripts/preview.py
"""

from __future__ import annotations

import http.server
import json
import os
import socketserver
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = 8080


def render_markdown_html(md_text: str) -> str:
    """Render markdown using GitHub's official markdown API with offline fallback."""
    try:
        req = urllib.request.Request(
            "https://api.github.com/markdown",
            data=json.dumps({"text": md_text, "mode": "gfm"}).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Zaid7829-Profile-Previewer",
            },
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            rendered_body = response.read().decode("utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] Online GitHub API render failed ({exc}), using raw layout fallback.")
        rendered_body = f"<pre style='white-space: pre-wrap; font-family: monospace;'>{md_text}</pre>"

    return f"""<!DOCTYPE html>
<html lang="en" data-color-mode="dark" data-dark-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Zaid7829 | GitHub Profile Preview</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown-dark.min.css">
  <style>
    body {{
      background-color: #0d1117;
      margin: 0;
      padding: 24px 16px;
      display: flex;
      justify-content: center;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
    }}
    .preview-container {{
      max-width: 1012px;
      width: 100%;
      background-color: #0d1117;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 32px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }}
    .preview-banner {{
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 10px 16px;
      margin-bottom: 24px;
      font-size: 13px;
      color: #8b949e;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
    }}
    .preview-banner span.online {{
      color: #3fb950;
    }}
    .markdown-body table {{
      display: table !important;
      width: 100% !important;
    }}
    .markdown-body img {{
      max-width: 100%;
    }}
  </style>
</head>
<body>
  <div class="preview-container">
    <div class="preview-banner">
      <div><strong>zaid@github:~$</strong> preview --target=README.md</div>
      <div><span class="online">●</span> LOCAL GITHUB VIEWPORT ACTIVE</div>
    </div>
    <article class="markdown-body">
      {rendered_body}
    </article>
  </div>
</body>
</html>
"""


class PreviewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):  # noqa: N802
        if self.path in ("/", "/index.html"):
            readme_path = ROOT / "README.md"
            if readme_path.exists():
                content = readme_path.read_text(encoding="utf-8")
                html = render_markdown_html(content).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html)))
                self.end_headers()
                self.wfile.write(html)
                return
        return super().do_GET()


def main():
    os.chdir(ROOT)
    handler = PreviewHandler

    # Find open port starting from PORT
    port = PORT
    server = None
    for p in range(PORT, PORT + 20):
        try:
            server = socketserver.TCPServer(("", p), handler)
            port = p
            break
        except OSError:
            continue

    if not server:
        print(f"[ERROR] Could not bind to any port in range {PORT}-{PORT+20}")
        sys.exit(1)

    url = f"http://localhost:{port}"
    print("=" * 60)
    print("  GitHub Profile Local Previewer")
    print(f"  URL: {url}")
    print("  Serving README.md rendered with GitHub Dark theme.")
    print("  Press Ctrl+C in terminal to stop.")
    print("=" * 60)

    # Open browser automatically after a short delay
    threading.Thread(target=lambda: (time.sleep(0.5), webbrowser.open(url)), daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down preview server...")
        server.server_close()


if __name__ == "__main__":
    main()
