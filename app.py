"""
Flask application entrypoint for Vercel.
This file serves as the main entrypoint for Vercel deployments.
"""

import os
import sys
from pathlib import Path
import importlib.util

# Get the path to the app package __init__.py
app_package_dir = Path(__file__).parent / 'app'
app_init_file = app_package_dir / '__init__.py'

try:
    # Load the app package directly from the directory to avoid circular import
    spec = importlib.util.spec_from_file_location("app_package", app_init_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load app package from {app_init_file}")

    app_package = importlib.util.module_from_spec(spec)
    sys.modules['app'] = app_package  # Register it as 'app' for submodules
    spec.loader.exec_module(app_package)

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