"""
API v1 initialization.
"""

from app.api import api_bp

# Import all API modules to register routes
from . import auth
from . import content
from . import search
from . import user

__all__ = ['auth', 'content', 'search', 'user']