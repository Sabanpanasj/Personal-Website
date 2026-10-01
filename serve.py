"""Test the website on your own computer.

Run:   python serve.py
Open:  http://localhost:8000

To test on your phone or tablet, connect it to the same Wi-Fi as this computer, then run:

    python serve.py <your-LAN-IP> <port>

For example, if `ipconfig` shows 192.168.1.42, run:

    python serve.py 192.168.1.42 8000

Then open http://192.168.1.42:8000 on the phone.

If you don't pass an IP, the server tries to auto-detect one and prints it.
To keep it private to this computer only, run:  python serve.py --local-only
Press Ctrl+C to stop.

If the phone still can't connect, allow Python through Windows Firewall:
  wf.msc  ->  Inbound Rules  ->  New Rule...  ->  Port
  ->  TCP  ->  8000  ->  Allow the connection  ->  Private  ->  name it.
"""
import socket
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from importlib import reload
from pathlib import Path
from urllib.parse import parse_qs

import build
import resume_data

ROOT = Path(__file__).parent
DIST = ROOT / "dist"


def rebuild():
    reload(resume_data)
    build.main()


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] in ("/", "/index.html", "/thanks.html"):
            try:
                rebuild()
            except Exception as err:
                print(f"Build failed: {err}")
        super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = parse_qs(self.rfile.read(length).decode("utf-8", "replace"))
        print("\n--- Contact form test (not emailed) ---")
        for key in ("name", "email", "message"):
            print(f"{key}: {data.get(key, [''])[0]}")
        print("---------------------------------------\n")
        self.path = "/thanks.html"
        super().do_GET()

    def log_message(self, fmt, *args):
        pass


def detect_lan_ip():
    """Return the IP the OS would use to reach the internet, or None."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return None


def is_lan_ip(ip):
    """True for RFC1918 private addresses, which are what we want for LAN testing."""
    return ip.startswith(("10.", "192.168.", "172."))


def can_bind(host, port):
    """Return True if we can actually listen on host:port right now."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
        return True
    except OSError:
        return False


def parse_args(argv):
    """Return (mode, host, port). mode is one of: 'local', 'lan', 'explicit'."""
    local_only = "--local-only" in argv
    if local_only:
        return "local", "127.0.0.1", 8000

    # Separate IP-looking args from port-looking args.
    ips = [a for a in argv if a.count(".") == 3 and not a.isdigit()]
    ports = [a for a in argv if a.isdigit()]

    port = int(ports[0]) if ports else 8000

    if ips:
        return "explicit", ips[0], port

    detected = detect_lan_ip()
    if detected and is_lan_ip(detected):
        return "lan", detected, port

    return "lan", "0.0.0.0", port


def main():
    mode, host, port = parse_args(sys.argv[1:])

    if not can_bind(host, port):
        # If the requested port is busy on the requested host, try nearby ports.
        for candidate in range(port + 1, port + 51):
            if can_bind(host, candidate):
                print(f"Port {port} was busy on {host}, using {candidate} instead.")
                port = candidate
                break
        else:
            raise SystemExit(
                f"Cannot bind to {host}:{port} (or {port + 1}-{port + 50}).\n"
                f"Another program is using them, or the IP is not on this machine.\n"
                f"Check `ipconfig` and pass the correct IP: python serve.py <IP> <port>"
            )

    rebuild()

    try:
        server = ThreadingHTTPServer((host, port), partial(Handler, directory=str(DIST)))
    except OSError as err:
        raise SystemExit(f"Could not start server on {host}:{port}: {err}")

    print(f"Site running at http://localhost:{port}  (Ctrl+C to stop)")

    if mode == "local":
        print("Mode: local-only (no other device can reach this).")
    else:
        if host == "0.0.0.0":
            print(f"Listening on all interfaces, port {port}.")
            print("Find your LAN IP with `ipconfig` (IPv4 Address of your Wi-Fi adapter)")
            print(f"and open http://<that-IP>:{port} on the phone.")
        else:
            print(f"On your phone (same Wi-Fi): http://{host}:{port}")

        print()
        print("If the phone says \"This site can't be reached\":")
        print("  1. Make sure both devices are on the same Wi-Fi and mobile data is OFF.")
        print("  2. Allow Python through Windows Firewall for Private networks:")
        print(f"     wf.msc -> Inbound Rules -> New Rule -> Port -> TCP -> {port} -> Allow.")
        print("  3. Set your Wi-Fi network profile to Private (Settings -> Network).")
        print("  4. Disconnect any VPN on the PC.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()