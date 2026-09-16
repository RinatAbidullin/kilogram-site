#!/usr/bin/env python3
"""Preview only public site files at /kilogram-site/, including nested 404s."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "/kilogram-site/"
PRODUCTION = "https://rinatabidullin.github.io/kilogram-site/"
PAGES = {"index.html", "404.html", "privacy/index.html", "terms/index.html",
         "support/index.html", "data-sources/index.html", "licenses/index.html"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond()

    def do_HEAD(self):
        self.respond(head=True)

    def respond(self, head=False):
        path = unquote(urlsplit(self.path).path)
        if path == PREFIX.rstrip("/"):
            self.send_response(301)
            self.send_header("Location", PREFIX)
            self.end_headers()
            return
        relative = path.removeprefix(PREFIX)
        if relative.endswith("/") or relative == "":
            relative += "index.html"
        file = (ROOT / relative).resolve()
        allowed = relative in PAGES or (
            relative.startswith("assets/") and file.suffix in {".png", ".css", ".js"})
        found = path.startswith(PREFIX) and allowed and file.is_relative_to(ROOT) and file.is_file()
        if not found:
            file = ROOT / "404.html"
        body = file.read_bytes()
        if file.name == "404.html":
            # GitHub serves this document at arbitrary missing paths. Its absolute
            # production URLs must use the preview origin during local checks.
            preview = f"http://127.0.0.1:{self.server.server_port}{PREFIX}"
            body = body.replace(PRODUCTION.encode(), preview.encode())
        self.send_response(200 if found else 404)
        self.send_header("Content-Type", mimetypes.guess_type(file)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head:
            self.wfile.write(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Kilogram preview: http://127.0.0.1:{args.port}{PREFIX}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
