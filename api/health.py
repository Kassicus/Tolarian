"""
Simple health check endpoint for debugging.
"""

from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {
            'status': 'healthy',
            'message': 'Health check endpoint is working',
            'environment': os.environ.get('VERCEL_ENV', 'unknown'),
            'path': self.path
        }

        self.wfile.write(json.dumps(response).encode())
        return