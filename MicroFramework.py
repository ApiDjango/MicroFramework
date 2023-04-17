import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import ssl

class MicroFrameworkHandler(BaseHTTPRequestHandler):
    routes = {}

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        path = parsed_url.path
        if path in self.routes:
            response_body = self.routes[path](query_params)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_body).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        request_body = self.rfile.read(content_length)
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        path = parsed_url.path
        if path in self.routes:
            response_body = self.routes[path](query_params, json.loads(request_body.decode('utf-8')))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_body).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode('utf-8'))

    @classmethod
    def route(cls, path):
        def wrapper(handler):
            cls.routes[path] = handler
            return handler
        return wrapper

def run_server(port, use_ssl=False, ssl_certfile=None, ssl_keyfile=None):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MicroFrameworkHandler)
    if use_ssl:
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=ssl_certfile, keyfile=ssl_keyfile, server_side=True)
    httpd.serve_forever()
