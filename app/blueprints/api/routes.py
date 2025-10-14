"""API routes (placeholder)."""
from flask import jsonify
from . import api_bp

@api_bp.route("/")
def index():
    return jsonify({"message": "API - To be implemented"})

@api_bp.route("/docs")
def docs():
    return jsonify({"message": "API documentation - To be implemented"})
