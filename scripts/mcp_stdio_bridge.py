"""Stdio-to-HTTP Model Context Protocol bridge for Unreal Engine.

Allows AI clients or tooling requiring Stdio transport to communicate
transparently with Unreal Engine's embedded ModelContextProtocol HTTP server
on loopback (default: http://127.0.0.1:8000/mcp).
"""

from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_ENDPOINT = os.environ.get("UNREAL_MCP_URL", "http://127.0.0.1:8000/mcp")


def main() -> int:
    endpoint = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ENDPOINT

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req_data = line.encode("utf-8")
            req = Request(
                endpoint,
                data=req_data,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
            with urlopen(req, timeout=30) as resp:
                resp_data = resp.read().decode("utf-8")
                sys.stdout.write(resp_data.strip() + "\n")
                sys.stdout.flush()
        except Exception as exc:
            try:
                parsed = json.loads(line)
                req_id = parsed.get("id")
            except Exception:
                req_id = None
            err_resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32603,
                    "message": f"Bridge error communicating with Unreal MCP at {endpoint}: {exc}",
                },
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

    return 0


if __name__ == "__main__":
    sys.exit(main())
