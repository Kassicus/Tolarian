"""Admin routes (placeholder)."""
from flask import jsonify
from . import admin_bp

@admin_bp.route("/")
def index():
    return jsonify({"message": "Admin - To be implemented"})

@admin_bp.route("/dashboard")
def dashboard():
    return jsonify({"message": "Admin dashboard - To be implemented"})
