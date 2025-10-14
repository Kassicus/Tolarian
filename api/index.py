"""
Main entry point for Vercel serverless deployment.
This file is the handler for all HTTP requests to the Flask application.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import app module
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from app import create_app

    # Create Flask application instance
    # Vercel will set VERCEL_ENV which we use to determine config
    if os.environ.get('VERCEL_ENV'):
        app = create_app('vercel')
    else:
        app = create_app('development')

    # Vercel expects a variable named 'app' as the entry point
    # The Flask app instance will be used by Vercel to handle requests

except Exception as e:
    # Create a minimal Flask app that shows the error
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route('/')
    @app.route('/<path:path>')
    def error_handler(path=''):
        return jsonify({
            'error': 'Application failed to initialize',
            'message': str(e),
            'type': type(e).__name__,
            'env_vars_set': {
                'VERCEL_ENV': bool(os.environ.get('VERCEL_ENV')),
                'SUPABASE_URL': bool(os.environ.get('SUPABASE_URL')),
                'SUPABASE_ANON_KEY': bool(os.environ.get('SUPABASE_ANON_KEY')),
                'SUPABASE_SERVICE_KEY': bool(os.environ.get('SUPABASE_SERVICE_KEY')),
                'DATABASE_URL': bool(os.environ.get('DATABASE_URL')),
                'SECRET_KEY': bool(os.environ.get('SECRET_KEY'))
            }
        }), 500