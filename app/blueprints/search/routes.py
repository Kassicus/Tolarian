"""Search routes (placeholder)."""
from flask import jsonify
from . import search_bp

@search_bp.route("/")
def index():
    return jsonify({"message": "Search - To be implemented"})

@search_bp.route("/search")
def search():
    return jsonify({"message": "Search - To be implemented"})
