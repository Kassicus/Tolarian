"""
Vercel serverless function handler for Flask application.
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from pathlib import Path

# Add parent directory to path to import app module
sys.path.insert(0, str(Path(__file__).parent.parent))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        self.handle_request()

    def do_POST(self):
        """Handle POST requests."""
        self.handle_request()

    def do_PUT(self):
        """Handle PUT requests."""
        self.handle_request()

    def do_DELETE(self):
        """Handle DELETE requests."""
        self.handle_request()

    def handle_request(self):
        """Process the request through Flask."""
        try:
            # Simple response for testing
            if self.path == '/api/health':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                response = {
                    'status': 'healthy',
                    'message': 'API is working',
                    'path': self.path,
                    'method': self.command
                }

                self.wfile.write(json.dumps(response).encode())
                return

            # Try to load Flask app
            if self.path.startswith('/api/v1'):
                try:
                    from flask import Flask, jsonify, request

                    # Create a minimal Flask app
                    app = Flask(__name__)

                    # Add a test route
                    @app.route('/api/v1/test')
                    def test():
                        return jsonify({
                            'status': 'ok',
                            'message': 'Flask endpoint working'
                        })

                    # Try to load the real app
                    try:
                        from app import create_app
                        app = create_app('production')

                        # Process the request through Flask
                        with app.test_request_context(
                            path=self.path,
                            method=self.command
                        ):
                            response = app.full_dispatch_request()

                            self.send_response(response.status_code)
                            for header, value in response.headers:
                                self.send_header(header, value)
                            self.end_headers()

                            self.wfile.write(response.get_data())
                            return

                    except Exception as e:
                        # If loading the real app fails, return error info
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()

                        error_response = {
                            'error': 'Failed to load Flask app',
                            'message': str(e),
                            'type': type(e).__name__,
                            'path': self.path
                        }

                        self.wfile.write(json.dumps(error_response).encode())
                        return

                except ImportError as e:
                    # Flask not available
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()

                    error_response = {
                        'error': 'Flask import failed',
                        'message': str(e),
                        'path': self.path
                    }

                    self.wfile.write(json.dumps(error_response).encode())
                    return

            # Default response for other paths
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = {
                'error': 'Not found',
                'path': self.path,
                'message': 'This endpoint does not exist'
            }

            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            # Last resort error handler
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            error_response = {
                'error': 'Handler error',
                'message': str(e),
                'type': type(e).__name__
            }

            self.wfile.write(json.dumps(error_response).encode())