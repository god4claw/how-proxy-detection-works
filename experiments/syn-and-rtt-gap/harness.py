#!/usr/bin/env python3
"""Server-side "ACK -> first ClientHello byte" measurement harness.

This is a deliberately small lab rig. It runs four TCP endpoints on one
Linux host:

    9443  target, reached directly
    9444  target, reached through the CONNECT proxy on 9080
    9445  target, reached through the SOCKS5 proxy on 9180
    9446  target, reached through a "slow" CONNECT proxy on 9280
          (the proxy waits 150 ms after connecting upstream, before it
          answers the client, i.e. after the target has already accepted)

Every target records two monotonic timestamps: the moment accept() returns
(final ACK of the TCP handshake) and the moment the first application byte
arrives (the first byte of a TLS ClientHello). The delta is what a server
can observe as the "TLS gap".

It is not a production proxy: no authentication, no DNS, no timeouts
beyond what is needed for the lab. Run it only on a host you control.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import socket
import struct
import threading
import time

STOP = threading.Event()


def now() -> float:
    return time.monotonic()


def append_json(path: str, obj: dict) -> None:
    line = json.dumps(obj, ensure_ascii=False, sort_keys=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def recv_exact(conn: socket.socket, size: int) -> bytes | None:
    buf = b""
    while len(buf) < size:
        chunk = conn.recv(size - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def read_http_head(conn: socket.socket, limit: int = 65536) -> bytes | None:
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = conn.recv(4096)
        if not chunk:
            return None
        buf += chunk
        if len(buf) > limit:
            return None
    return buf


def relay(src: socket.socket, dst: socket.socket) -> None:
    try:
        while True:
            data = src.recv(65536)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    finally:
        try:
            dst.shutdown(socket.SHUT_WR)
        except OSError:
            pass


def run_relay(a: socket.socket, b: socket.socket) -> None:
    threads = [
        threading.Thread(target=relay, args=(a, b), daemon=True),
        threading.Thread(target=relay, args=(b, a), daemon=True),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=30)


class Target(threading.Thread):
    """Accepts one connection at a time and measures accept -> first byte."""

    def __init__(self, port: int, mode: str, log_path: str) -> None:
        super().__init__(daemon=True, name=f"target-{mode}")
        self.port = port
        self.mode = mode
        self.log_path = log_path
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(128)
        self.sock.settimeout(0.5)

    def run(self) -> None:
        while not STOP.is_set():
            try:
                conn, addr = self.sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            t_accept = now()
            threading.Thread(
                target=self._handle, args=(conn, addr, t_accept), daemon=True
            ).start()
        self.sock.close()

    def _handle(self, conn: socket.socket, addr, t_accept: float) -> None:
        record = {
            "mode": self.mode,
            "port": self.port,
            "peer": addr[0],
            "peer_port": addr[1],
            "t_accept": t_accept,
            "wall_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        try:
            conn.settimeout(20.0)
            first = conn.recv(1)
            t_first = now()
            record["t_first"] = t_first
            record["gap_ms"] = round((t_first - t_accept) * 1000.0, 4)
            record["first_byte"] = first.hex() if first else None
        except Exception as exc:  # noqa: BLE001 - lab rig, log everything
            record["error"] = f"{type(exc).__name__}: {exc}"
        finally:
            try:
                conn.close()
            except OSError:
                pass
            append_json(self.log_path, record)


class ConnectProxy(threading.Thread):
    def __init__(
        self,
        port: int,
        target_port: int,
        mode: str,
        delay_after_connect: float = 0.0,
    ) -> None:
        super().__init__(daemon=True, name=f"connect-{mode}")
        self.port = port
        self.target_port = target_port
        self.mode = mode
        self.delay = delay_after_connect
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(128)
        self.sock.settimeout(0.5)

    def run(self) -> None:
        while not STOP.is_set():
            try:
                conn, _ = self.sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(target=self._handle, args=(conn,), daemon=True).start()
        self.sock.close()

    def _handle(self, conn: socket.socket) -> None:
        upstream = None
        try:
            conn.settimeout(20.0)
            if read_http_head(conn) is None:
                return
            upstream = socket.create_connection(("127.0.0.1", self.target_port), 5)
            upstream.settimeout(20.0)
            if self.delay:
                # Processing after the upstream handshake is done:
                # the target has already accepted, but no bytes have
                # been relayed yet. This models a proxy that buffers,
                # logs or re-encrypts before it answers.
                time.sleep(self.delay)
            conn.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")
            run_relay(conn, upstream)
        except OSError:
            pass
        finally:
            for sock in (conn, upstream):
                try:
                    if sock is not None:
                        sock.close()
                except OSError:
                    pass


class Socks5Proxy(threading.Thread):
    def __init__(self, port: int, target_port: int) -> None:
        super().__init__(daemon=True, name="socks5")
        self.port = port
        self.target_port = target_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(128)
        self.sock.settimeout(0.5)

    def run(self) -> None:
        while not STOP.is_set():
            try:
                conn, _ = self.sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(target=self._handle, args=(conn,), daemon=True).start()
        self.sock.close()

    def _handle(self, conn: socket.socket) -> None:
        upstream = None
        try:
            conn.settimeout(20.0)
            head = recv_exact(conn, 2)
            if head is None or head[0] != 5:
                return
            recv_exact(conn, head[1])  # methods
            conn.sendall(b"\x05\x00")  # no auth
            req = recv_exact(conn, 4)
            if req is None:
                return
            atyp = req[3]
            if atyp == 1:
                recv_exact(conn, 4)
            elif atyp == 3:
                length = recv_exact(conn, 1)
                if length is None:
                    return
                recv_exact(conn, length[0])
            elif atyp == 4:
                recv_exact(conn, 16)
            else:
                return
            recv_exact(conn, 2)  # port
            upstream = socket.create_connection(("127.0.0.1", self.target_port), 5)
            upstream.settimeout(20.0)
            conn.sendall(b"\x05\x00\x00\x01" + b"\x00" * 6)  # bound 0.0.0.0:0
            run_relay(conn, upstream)
        except OSError:
            pass
        finally:
            for sock in (conn, upstream):
                try:
                    if sock is not None:
                        sock.close()
                except OSError:
                    pass


def stop(*_args) -> None:
    STOP.set()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", default="results", help="directory for JSONL logs")
    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    targets = [
        Target(9443, "direct", os.path.join(args.outdir, "direct.jsonl")),
        Target(9444, "connect", os.path.join(args.outdir, "connect.jsonl")),
        Target(9445, "socks5", os.path.join(args.outdir, "socks5.jsonl")),
        Target(9446, "connect-delayed", os.path.join(args.outdir, "connect-delayed.jsonl")),
    ]
    proxies = [
        ConnectProxy(9080, 9444, "connect"),
        Socks5Proxy(9180, 9445),
        ConnectProxy(9280, 9446, "connect-delayed", delay_after_connect=0.150),
    ]
    for thread in proxies:
        thread.start()
    for thread in targets:
        thread.start()
    print(f"harness up, logs in {os.path.abspath(args.outdir)}", flush=True)
    while not STOP.is_set():
        time.sleep(0.2)
    print("harness stopping", flush=True)


if __name__ == "__main__":
    main()
