"""Content routes (placeholder)."""
from flask import jsonify
from . import content_bp

@content_bp.route('/')
def index():
    return jsonify({"message": "Content - To be implemented"})

@content_bp.route('/list')
def list():
    return jsonify({"message": "Content list - To be implemented"})

@content_bp.route('/my')
def my_content():
    return jsonify({"message": "My content - To be implemented"})