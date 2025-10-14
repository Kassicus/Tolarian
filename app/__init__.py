"""
Knowledge Base Application
A centralized, searchable knowledge base for development teams.
"""

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Initialize extensions
login_manager = LoginManager()
migrate = Migrate()
cache = Cache()

# Database session management
db_session = None


def create_app(config_name=None):
    """Application factory pattern for Flask app creation."""
    import os
    from pathlib import Path

    # Get the absolute path to the app directory
    app_dir = Path(__file__).parent
    template_folder = app_dir / 'templates'
    static_folder = app_dir / 'static'

    app = Flask(__name__,
                template_folder=str(template_folder),
                static_folder=str(static_folder))

    # Load configuration
    from app.config import config_dict
    if config_name:
        config_class = config_dict.get(config_name)
        if config_class:
            app.config.from_object(config_class)
        else:
            # Fallback to development if config name not found
            app.config.from_object(config_dict['development'])
    else:
        # Default to development config if not specified
        app.config.from_object(config_dict['development'])

    # Initialize database session (if DATABASE_URL is configured)
    global db_session
    if app.config.get('DATABASE_URL'):
        engine = create_engine(app.config['DATABASE_URL'])
        db_session = scoped_session(sessionmaker(bind=engine))
    else:
        # No database configured yet - this is okay for initial setup
        engine = None
        db_session = None

    # Initialize extensions with app
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """Load user from Supabase by ID."""
        from app.utils.supabase import get_supabase_admin_client
        from app.models import User
        from app.models.user import UserRole

        try:
            client = get_supabase_admin_client()
            result = client.table('users').select('*').eq('id', user_id).execute()

            if result.data and len(result.data) > 0:
                user_data = result.data[0]

                # Create User object from Supabase data
                user = User()
                user.id = user_data['id']
                user.email = user_data['email']
                user.username = user_data.get('username')
                user.full_name = user_data.get('full_name')
                user.password_hash = user_data.get('password_hash')
                user.role = UserRole(user_data.get('role', 'viewer'))
                user.is_active = user_data.get('is_active', True)
                user.avatar_url = user_data.get('avatar_url')
                user.bio = user_data.get('bio')
                user.location = user_data.get('location')
                user.website = user_data.get('website')

                return user if user.is_active else None

        except Exception as e:
            print(f"Error loading user {user_id}: {e}")

        return None

    migrate.init_app(app, compare_type=True)

    cache.init_app(app, config={
        'CACHE_TYPE': app.config.get('CACHE_TYPE', 'simple'),
        'CACHE_DEFAULT_TIMEOUT': app.config.get('CACHE_DEFAULT_TIMEOUT', 300)
    })

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Register template filters
    register_template_filters(app)

    # Setup database teardown
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if db_session:
            db_session.remove()

    # Create tables if they don't exist (for development)
    if app.config.get('CREATE_TABLES_ON_START') and engine:
        with app.app_context():
            from app.models import create_all_tables
            create_all_tables(engine)

    return app


def register_blueprints(app):
    """Register all application blueprints."""
    from app.blueprints.main import main_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.content import content_bp
    from app.blueprints.search import search_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(content_bp, url_prefix='/content')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api/v1')


def register_error_handlers(app):
    """Register error handlers for common HTTP errors."""

    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        from flask import render_template
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        if db_session:
            db_session.rollback()
        return render_template('errors/500.html'), 500


def register_template_filters(app):
    """Register custom Jinja2 template filters."""
    from app.utils.filters import markdown_filter, datetime_filter, slugify_filter

    app.jinja_env.filters['markdown'] = markdown_filter
    app.jinja_env.filters['datetime'] = datetime_filter
    app.jinja_env.filters['slugify'] = slugify_filter