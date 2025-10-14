"""
Flask application entrypoint.
This file serves as a fallback entrypoint for Vercel if api/index.py is not found.
Also used for other deployment platforms that look for app.py.
"""

import os
from app import create_app

# Create Flask application instance
# Detect environment from VERCEL_ENV or FLASK_ENV
if os.environ.get('VERCEL_ENV'):
    app = create_app('vercel')
else:
    env = os.environ.get('FLASK_ENV', 'production')
    app = create_app(env)

# Expose app variable for WSGI servers
if __name__ == '__main__':
    # Only runs in local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.debug)