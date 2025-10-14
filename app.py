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

    # Debug: Check what's in the app_package
    if not hasattr(app_package, 'create_app'):
        # Try to get more info about what went wrong
        available_attrs = dir(app_package)
        raise ImportError(
            f"app package imported but create_app not found. "
            f"Available attributes: {', '.join(available_attrs[:20])}. "
            f"Package file: {app_package.__file__ if hasattr(app_package, '__file__') else 'unknown'}"
        )

    # Get the create_app function from the package
    create_app_func = app_package.create_app

    # Create Flask application instance
    # Detect environment from VERCEL_ENV or FLASK_ENV
    if os.environ.get('VERCEL_ENV'):
        app = create_app_func('vercel')
    else:
        env = os.environ.get('FLASK_ENV', 'production')
        app = create_app_func(env)

except Exception as init_error:
    # Create a minimal Flask app that shows the error
    from flask import Flask
    import traceback

    # Capture error details
    error_type = type(init_error).__name__
    error_message = str(init_error)
    error_traceback = traceback.format_exc()

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
                <p><strong>Error Type:</strong> {error_type}</p>
                <p><strong>Error Message:</strong> {error_message}</p>
                <h2>Full Traceback:</h2>
                <pre>{error_traceback}</pre>
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