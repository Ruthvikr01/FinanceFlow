"""Standalone health check server for monitoring tools.

Serves /health and /_stcore/health on port 8502 by default.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in {"/health", "/_stcore/health"}:
            payload = {
                "status": "ok",
                "service": "personalfinanceanalyzer",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            body = json.dumps(payload).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        # Keep health server logs quiet; app logging already captures service-level info.
        return


def run_health_server(port: int = 8502) -> None:
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


if __name__ == "__main__":
    run_health_server(int(os.getenv("HEALTH_CHECK_PORT", "8502")))
