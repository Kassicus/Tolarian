"""
Main entry point for Vercel serverless deployment.
This file is the handler for all HTTP requests to the Flask application.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import app module
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app

# Create Flask application instance
# Vercel will set VERCEL_ENV which we use to determine config
if os.environ.get('VERCEL_ENV'):
    app = create_app('vercel')
else:
    app = create_app('development')

# Vercel expects a variable named 'app' as the entry point
# The Flask app instance will be used by Vercel to handle requests