#!/usr/bin/env python3
"""Simple local dev server for AeroVista website."""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()

    def log_message(self, fmt, *args):
        print(f"  [{self.address_string()}] {args[0]} {args[1]} {args[2]}")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

if __name__ == '__main__':
    port = 8080
    ip = get_local_ip()
    server = HTTPServer(('0.0.0.0', port), CORSRequestHandler)
    print(f"""
  \033[1;33m✈ AeroVista — Drone Photography Website\033[0m
  \033[90m{'─' * 50}\033[0m
  \033[1;32m  Local:\033[0m   http://localhost:{port}
  \033[1;32m  Network:\033[0m http://{ip}:{port}
  \033[90m{'─' * 50}\033[0m
  \033[90m  Press Ctrl+C to stop\033[0m
    """)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Server stopped.')
        server.server_close()
