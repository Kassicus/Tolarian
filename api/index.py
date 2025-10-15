"""
Vercel serverless function handler for Flask application.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import app module
sys.path.insert(0, str(Path(__file__).parent.parent))

def handler(request):
    """
    Vercel serverless function handler.
    This is the entry point for all API requests.
    """
    try:
        # Import Flask app
        from flask import Flask, jsonify

        # Create a simple Flask app for testing
        app = Flask(__name__)

        # Test route
        @app.route('/api/test')
        def test():
            return jsonify({
                'status': 'ok',
                'message': 'Flask is working',
                'env': os.environ.get('VERCEL_ENV', 'unknown')
            })

        # Health check
        @app.route('/api/health')
        def health():
            return jsonify({
                'status': 'healthy',
                'environment': os.environ.get('VERCEL_ENV', 'unknown')
            })

        # Try to import the actual app
        try:
            from app import create_app

            # Use the actual app if it loads
            real_app = create_app('production')

            # Copy routes from real app to our test app
            for rule in real_app.url_map.iter_rules():
                app.add_url_rule(
                    rule.rule,
                    endpoint=rule.endpoint,
                    view_func=real_app.view_functions.get(rule.endpoint),
                    methods=rule.methods
                )

        except Exception as e:
            # If the real app fails, add an error endpoint
            @app.route('/api/error')
            def error():
                return jsonify({
                    'error': 'Failed to load main app',
                    'message': str(e),
                    'type': type(e).__name__
                }), 500

        # Create a test request context and process the request
        with app.test_request_context(
            path=request.path if hasattr(request, 'path') else '/api/health',
            method=request.method if hasattr(request, 'method') else 'GET'
        ):
            try:
                # Get the response from Flask
                response = app.full_dispatch_request()

                # Convert Flask response to Vercel format
                return {
                    'statusCode': response.status_code,
                    'headers': dict(response.headers) if response.headers else {'Content-Type': 'application/json'},
                    'body': response.get_data(as_text=True)
                }

            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': {
                        'error': 'Request processing failed',
                        'message': str(e)
                    }
                }

    except Exception as e:
        # Last resort error handler
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': {
                'error': 'Handler failed',
                'message': str(e),
                'type': type(e).__name__
            }
        }