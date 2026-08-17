#!/usr/bin/env python3
"""
Minimal HTTP server for PySwitch web editor.
Replaces Apache + PHP: handles toc.php requests and serves static files.

Usage:
    python serve.py [port]      default port: 8080

Open Chrome at http://localhost:8080
(Chrome required for Web MIDI API)
"""
import http.server
import json
import mimetypes
import sys
import threading
import time
import urllib.parse
from pathlib import Path

# Explicit MIME type table — overrides the Windows registry which often maps
# .js to text/html, causing Chrome to refuse script execution.
_MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".htm":  "text/html; charset=utf-8",
    ".css":  "text/css",
    ".js":   "application/javascript",
    ".mjs":  "application/javascript",
    ".json": "application/json",
    ".wasm": "application/wasm",
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif":  "image/gif",
    ".svg":  "image/svg+xml",
    ".ico":  "image/x-icon",
    ".woff": "font/woff",
    ".woff2":"font/woff2",
    ".ttf":  "font/ttf",
    ".otf":  "font/otf",
    ".eot":  "application/vnd.ms-fontobject",
    ".txt":  "text/plain",
    ".py":   "text/plain",
    ".md":   "text/plain",
    ".map":  "application/json",
}

BASE_DIR = Path(__file__).parent.resolve()
HTDOCS   = BASE_DIR / "htdocs"
CONTENT  = BASE_DIR.parent / "content"
EXAMPLES = BASE_DIR.parent / "examples"

# Order matters: longest prefix first
MOUNTS = [
    ("/circuitpy", CONTENT),
    ("/examples",  EXAMPLES),
]

def resolve_path(url_path: str) -> Path:
    """Map a URL path to a filesystem path, honouring volume mounts."""
    for prefix, fs_root in MOUNTS:
        if url_path == prefix or url_path.startswith(prefix + "/"):
            rel = url_path[len(prefix):].lstrip("/")
            return fs_root / rel
    return HTDOCS / url_path.lstrip("/")


def make_toc(directory: Path) -> dict:
    """
    Replicate the JSON output of toc.php.
    {"type":"dir","name":"","path":"","children":[...]}
    """
    def fill(d: Path) -> list:
        nodes = []
        try:
            entries = sorted(d.iterdir(), key=lambda e: (e.is_file(), e.name))
        except PermissionError:
            return nodes
        for entry in entries:
            if entry.name.startswith("."):
                continue
            if entry.is_dir():
                nodes.append({"type": "dir", "name": entry.name,
                               "children": fill(entry)})
            elif entry.is_file():
                nodes.append({"type": "file", "name": entry.name})
        return nodes

    return {"type": "dir", "name": "", "path": "",
            "children": fill(directory)}


class PySwitchHandler(http.server.BaseHTTPRequestHandler):

    def do_HEAD(self):
        # Reuse GET logic but discard the body
        self._head_only = True
        self.do_GET()
        self._head_only = False

    def do_GET(self):
        if not hasattr(self, '_head_only'):
            self._head_only = False
        parsed   = urllib.parse.urlparse(self.path)
        url_path = urllib.parse.unquote(parsed.path)
        fs_path  = resolve_path(url_path)

        # ---- toc.php -------------------------------------------------------
        if fs_path.name == "toc.php":
            directory = fs_path.parent
            if not directory.is_dir():
                self._send_error(404, f"Directory not found: {directory}")
                return
            body = json.dumps(make_toc(directory), separators=(",", ":")).encode()
            self._send_bytes(body, "application/json")
            return

        # ---- directory → index.html ----------------------------------------
        if fs_path.is_dir():
            fs_path = fs_path / "index.html"

        # ---- static file ---------------------------------------------------
        if not fs_path.exists() or not fs_path.is_file():
            self._send_error(404, f"Not found: {url_path}")
            return

        suffix = fs_path.suffix.lower()
        content_type = _MIME_TYPES.get(suffix) or mimetypes.guess_type(str(fs_path))[0] or "application/octet-stream"
        try:
            data = fs_path.read_bytes()
        except OSError as exc:
            self._send_error(500, str(exc))
            return
        self._send_bytes(data, content_type)

    # ------------------------------------------------------------------
    def _send_bytes(self, data: bytes, content_type: str):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if not self._head_only:
            self.wfile.write(data)

    def _send_error(self, code: int, msg: str = ""):
        body = msg.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def handle_error(self, request, client_address):
        # Silently ignore abrupt client disconnections (e.g. browser reload/cancel).
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionResetError, BrokenPipeError)):
            return
        super().handle_error(request, client_address)

    def log_message(self, fmt, *args):
        # Log everything so we can spot 404s and errors in the terminal
        super().log_message(fmt, *args)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9090
    server = http.server.HTTPServer(("0.0.0.0", port), PySwitchHandler)
    url = f"http://localhost:{port}"
    print(f"PySwitch editor running at  {url}")
    print("Open this URL in Chrome (required for Web MIDI)")
    print("Press Ctrl+C to stop\n")
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    try:
        while t.is_alive():
            time.sleep(0.5)
    except KeyboardInterrupt:
        server.shutdown()
        print("\nStopped.")
