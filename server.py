#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket, urllib.parse, json, os
from datetime import datetime

TO_EMAIL = "atticus.a@zohomail.com"
BOOKINGS_FILE = "bookings.json"

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()

    def log_message(self, fmt, *args):
        print(f"  [{self.address_string()}] {args[0]} {args[1]} {args[2]}")

    def do_POST(self):
        if self.path == '/send-email':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            data = urllib.parse.parse_qs(body)

            booking = {
                "time": datetime.now().isoformat(),
                "name": data.get('name', [''])[0],
                "email": data.get('email', [''])[0],
                "message": data.get('message', [''])[0]
            }

            bookings = []
            if os.path.exists(BOOKINGS_FILE):
                try:
                    with open(BOOKINGS_FILE) as f:
                        bookings = json.load(f)
                except:
                    pass
            bookings.append(booking)
            with open(BOOKINGS_FILE, 'w') as f:
                json.dump(bookings, f, indent=2)

            print(f"\n  New booking: {booking['name']} <{booking['email']}>")
            print(f"  {booking['message']}\n")

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_response(404)
            self.end_headers()

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
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"""
  \033[1;36mBurlington Drone Photos\033[0m
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
