"""
Vercel serverless function handler for Flask application.
Uses WSGI adapter for Vercel Python runtime.
"""

import os
import sys
from pathlib import Path

# Add parent's parent directory to path to import app module
# frontend/api -> frontend -> root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from app import create_app

    # Create Flask application instance
    if os.environ.get('VERCEL_ENV'):
        app = create_app('vercel')
    else:
        app = create_app('production')

except Exception as e:
    # Fallback error handler
    from flask import Flask
    import traceback

    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        error_details = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Application Error</title>
            <style>
                body {{ font-family: monospace; padding: 20px; background: #f5f5f5; }}
                .error {{ background: white; padding: 20px; border-radius: 5px; border: 2px solid #dc3545; }}
                h1 {{ color: #dc3545; }}
                pre {{ background: #f8f9fa; padding: 10px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>⚠️ Application Failed to Initialize</h1>
                <p><strong>Error Type:</strong> {type(e).__name__}</p>
                <p><strong>Error Message:</strong> {str(e)}</p>
                <h2>Traceback:</h2>
                <pre>{traceback.format_exc()}</pre>
                <h2>Environment Check:</h2>
                <ul>
                    <li>VERCEL_ENV: {os.environ.get('VERCEL_ENV', 'Not Set')}</li>
                    <li>PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not Set')}</li>
                    <li>DATABASE_URL: {'Set' if os.environ.get('DATABASE_URL') else 'Not Set'}</li>
                    <li>SECRET_KEY: {'Set' if os.environ.get('SECRET_KEY') else 'Not Set'}</li>
                </ul>
            </div>
        </body>
        </html>
        """
        return error_details, 500

# Vercel expects the app to be exposed directly
# The WSGI app will be handled by Vercel's Python runtime