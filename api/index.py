"""
Main entry point for Vercel serverless deployment.
This file is the handler for all HTTP requests to the Flask application.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import app module
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Remove current directory from path to avoid importing this file as 'app'
current_dir = str(Path(__file__).parent)
if current_dir in sys.path:
    sys.path.remove(current_dir)

try:
    # Import from the app package (directory), not this file
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
    from flask import Flask
    import traceback

    app = Flask(__name__)

    @app.route('/')
    @app.route('/<path:path>')
    def error_handler(path=''):
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Application Error</title>
            <style>
                body {{ font-family: monospace; padding: 20px; background: #f5f5f5; }}
                .error {{ background: white; padding: 20px; border-radius: 5px; border: 2px solid #dc3545; }}
                h1 {{ color: #dc3545; }}
                .env-check {{ margin-top: 20px; }}
                .env-item {{ padding: 5px; margin: 5px 0; }}
                .set {{ color: green; }}
                .missing {{ color: red; }}
                pre {{ background: #f8f9fa; padding: 10px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>⚠️ Application Failed to Initialize</h1>
                <p><strong>Error Type:</strong> {type(e).__name__}</p>
                <p><strong>Error Message:</strong> {str(e)}</p>

                <div class="env-check">
                    <h2>Environment Variables Check:</h2>
                    <div class="env-item {'set' if os.environ.get('VERCEL_ENV') else 'missing'}">
                        VERCEL_ENV: {'✓ Set' if os.environ.get('VERCEL_ENV') else '✗ Missing'}
                    </div>
                    <div class="env-item {'set' if os.environ.get('SUPABASE_URL') else 'missing'}">
                        SUPABASE_URL: {'✓ Set' if os.environ.get('SUPABASE_URL') else '✗ Missing'}
                    </div>
                    <div class="env-item {'set' if os.environ.get('SUPABASE_ANON_KEY') else 'missing'}">
                        SUPABASE_ANON_KEY: {'✓ Set' if os.environ.get('SUPABASE_ANON_KEY') else '✗ Missing'}
                    </div>
                    <div class="env-item {'set' if os.environ.get('SUPABASE_SERVICE_KEY') else 'missing'}">
                        SUPABASE_SERVICE_KEY: {'✓ Set' if os.environ.get('SUPABASE_SERVICE_KEY') else '✗ Missing'}
                    </div>
                    <div class="env-item {'set' if os.environ.get('DATABASE_URL') else 'missing'}">
                        DATABASE_URL: {'✓ Set' if os.environ.get('DATABASE_URL') else '✗ Missing'}
                    </div>
                    <div class="env-item {'set' if os.environ.get('SECRET_KEY') else 'missing'}">
                        SECRET_KEY: {'✓ Set' if os.environ.get('SECRET_KEY') else '✗ Missing'}
                    </div>
                </div>

                <h2>Full Traceback:</h2>
                <pre>{traceback.format_exc()}</pre>
            </div>
        </body>
        </html>
        """
        return error_html, 500