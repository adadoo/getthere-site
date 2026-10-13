"""The website's own server: the website (getthere.now) is the Direct channel's app, so it gets its
forward address the way a card issuer's app does, from GetThere's partner API with a channel key
(Dadoo, 2026-10-13). The key is a secret, so it lives here and never in the pages.

    POST /offer?utm_source=..&utm_medium=..&utm_campaign=..&ref=<the page's referrer>
        site.js calls this when the home page opens. It asks GET /partner/v1/offer for a new offer,
        passing the page's utm tags and referring site, with opened=true (the page shows the address
        itself), and answers {"forward_to": "quote+<id>@my.getthere.now", "reference": "R-<ID>"}.
    GET  /health
        Up.

Settings (environment):
    GETTHERE_PARTNER_KEY   the Direct channel's key from the admin (gt_live_... or gt_test_...)
    GETTHERE_API_URL       default https://api.getthere.now/partner/v1
    ALLOWED_ORIGINS        pages that may call it, comma separated; default https://getthere.now
    PORT                   default 8000

Standard library only. Run locally:  GETTHERE_PARTNER_KEY=gt_test_... python3 server.py
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

API_URL = os.environ.get("GETTHERE_API_URL", "https://api.getthere.now/partner/v1").rstrip("/")
KEY = os.environ.get("GETTHERE_PARTNER_KEY", "")
ORIGINS = {o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "https://getthere.now").split(",") if o.strip()}
PASSED_ON = ("utm_source", "utm_medium", "utm_campaign", "src")    # the partner API cleans them


def new_offer(query):
    """A new offer from the partner API for the page's query ({name: value}), or None."""
    params = {k: query[k][:200] for k in PASSED_ON if query.get(k)}
    if query.get("ref"):
        params["referrer_url"] = query["ref"][:500]
    params["opened"] = "true"
    req = urllib.request.Request(f"{API_URL}/offer?{urllib.parse.urlencode(params)}",
                                 headers={"Authorization": f"Bearer {KEY}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            offer = json.load(r)
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        print(f"partner API: {e}", file=sys.stderr)
        return None
    return {"forward_to": offer["forward_to"], "reference": offer["reference"]}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body=None):
        self.send_response(status)
        origin = self.headers.get("Origin")
        if origin in ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Cache-Control", "no-store")
        data = json.dumps(body).encode() if body is not None else b""
        if body is not None:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"ok": True, "key": bool(KEY)})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        url = urllib.parse.urlsplit(self.path)
        if url.path != "/offer":
            return self._send(404, {"error": "not found"})
        if self.headers.get("Origin") not in ORIGINS:      # only our own pages make offers
            return self._send(403, {"error": "origin not allowed"})
        if not KEY:
            return self._send(503, {"error": "no partner key set"})
        query = {k: v[0] for k, v in urllib.parse.parse_qs(url.query).items()}
        offer = new_offer(query)
        self._send(200, offer) if offer else self._send(502, {"error": "partner API unavailable"})

    def log_message(self, fmt, *args):
        print(f"{self.command} {urllib.parse.urlsplit(self.path).path} {args[1] if len(args) > 1 else ''}",
              file=sys.stderr)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"listening on {port}, partner API {API_URL}, key {'set' if KEY else 'missing'}", file=sys.stderr)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
