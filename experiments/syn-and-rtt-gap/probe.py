#!/usr/bin/env python3
"""Client for harness.py: runs the same HTTPS request through four paths.

    direct           https://127.0.0.1:9443/
    connect          curl -x http://127.0.0.1:9080
    socks5           curl --socks5-hostname 127.0.0.1:9180
    connect-delayed  curl -x http://127.0.0.1:9280

The target closes the connection after the first ClientHello byte, so each
curl run ends with a TLS error. That is expected: only the server-side
timestamps are measured. Client-side curl timings are written to
client.csv as a sanity check, not as the primary measurement.

Run this from the same host as harness.py for the loopback run, or from a
remote host (with --host pointing at the harness host) for a WAN run.
"""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import time

CASES = {
    # name: (URL, curl args)
    "direct": ("https://{host}:9443/", []),
    "connect": (
        "https://target.invalid:9443/",
        ["-x", "http://{host}:9080"],
    ),
    "socks5": (
        "https://target.invalid:9443/",
        ["--socks5-hostname", "{host}:9180"],
    ),
    "connect-delayed": (
        "https://target.invalid:9443/",
        ["-x", "http://{host}:9280"],
    ),
}


def run_one(host: str, name: str) -> dict:
    url, extra = CASES[name]
    cmd = [
        "curl",
        "-sk",
        "-o",
        os.devnull,
        "--max-time",
        "5",
        "-w",
        "%{time_connect},%{time_appconnect},%{time_total}",
    ]
    cmd += [part.format(host=host) for part in extra]
    cmd.append(url.format(host=host))
    started = time.monotonic()
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    elapsed = time.monotonic() - started
    return {
        "mode": name,
        "exit_code": proc.returncode,
        "client_connect_s": "",
        "client_appconnect_s": "",
        "client_total_s": "",
        "wall_s": round(elapsed, 4),
        "curl_stderr": proc.stderr.strip()[-300:],
    } | dict(zip(("client_connect_s", "client_appconnect_s", "client_total_s"), proc.stdout.strip().split(",")))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--iterations", type=int, default=30)
    parser.add_argument("--out", default="results/client.csv")
    args = parser.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)

    rows = []
    for iteration in range(args.iterations):
        for name in CASES:
            rows.append({"iteration": iteration + 1, **run_one(args.host, name)})
            time.sleep(0.02)
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {os.path.abspath(args.out)}")


if __name__ == "__main__":
    main()
