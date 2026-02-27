from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'service': 'events-svc-s11',
            'resource': 'events',
            'port': 8257,
            'message': 'Hello from events service!'
        }
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        response = {
            'service': 'events-svc-s11',
            'resource': 'events',
            'port': 8257,
            'received': json.loads(post_data.decode()),
            'message': 'Event created!'
        }
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8257), Handler)
    print('Starting events service on port 8257...')
    server.serve_forever()