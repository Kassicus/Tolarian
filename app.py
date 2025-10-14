"""
Flask application entrypoint for Vercel.
This file serves as the main entrypoint for Vercel deployments.
"""

import os
import sys
from pathlib import Path

# Ensure the app package can be imported
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    # Import from app package (directory named 'app')
    import app as app_package

    # Get the create_app function from the package
    create_app_func = app_package.create_app

    # Create Flask application instance
    # Detect environment from VERCEL_ENV or FLASK_ENV
    if os.environ.get('VERCEL_ENV'):
        app = create_app_func('vercel')
    else:
        env = os.environ.get('FLASK_ENV', 'production')
        app = create_app_func(env)

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
                pre {{ background: #f8f9fa; padding: 10px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>⚠️ Application Failed to Initialize</h1>
                <p><strong>Error Type:</strong> {type(e).__name__}</p>
                <p><strong>Error Message:</strong> {str(e)}</p>
                <h2>Full Traceback:</h2>
                <pre>{traceback.format_exc()}</pre>
            </div>
        </body>
        </html>
        """
        return error_html, 500

# Expose app variable for WSGI servers
if __name__ == '__main__':
    # Only runs in local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.debug)