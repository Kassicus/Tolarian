"""
Main routes for the Knowledge Base application.
"""

from flask import render_template, current_app
from flask_login import current_user
from . import main_bp


@main_bp.route('/')
def index():
    """Home page route."""
    return render_template('main/index.html')


@main_bp.route('/about')
def about():
    """About page route."""
    return render_template('main/about.html')


@main_bp.route('/help')
def help():
    """Help page route."""
    return render_template('main/help.html')


@main_bp.route('/dashboard')
def dashboard():
    """User dashboard route."""
    # Will implement after authentication is set up
    return render_template('main/dashboard.html')