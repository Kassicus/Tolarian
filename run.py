#!/usr/bin/env python
"""
Local development entry point for the Knowledge Base application.
This script is used to run the Flask application in development mode.
"""

import os
import sys
from app import create_app

# Create Flask application with development config
app = create_app('development')

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))

    # Get host from environment or use default
    host = os.environ.get('HOST', '127.0.0.1')

    # Check if we should run in debug mode
    debug = os.environ.get('FLASK_ENV') == 'development'

    print(f"""
    ====================================
    Knowledge Base Application
    ====================================
    Running on: http://{host}:{port}
    Debug mode: {'ON' if debug else 'OFF'}
    Press CTRL+C to quit
    ====================================
    """)

    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )