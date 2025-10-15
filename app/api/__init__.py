"""
API package initialization.
"""

from flask import Blueprint

# Create API blueprint
api_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Import API routes to register them
from app.api.v1 import auth, content, search, user

__all__ = ['api_bp']