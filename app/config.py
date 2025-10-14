"""
Configuration settings for the Knowledge Base application.
Supports development, testing, and production environments.
"""

import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env.local or .env file
base_dir = Path(__file__).parent.parent
env_file = base_dir / '.env.local' if (base_dir / '.env.local').exists() else base_dir / '.env'
load_dotenv(env_file)


class Config:
    """Base configuration with settings common to all environments."""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Supabase settings
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
    SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')

    # Database settings (Direct PostgreSQL connection for migrations)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        # Fix for SQLAlchemy requiring postgresql:// instead of postgres://
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # File upload settings
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
    ALLOWED_EXTENSIONS = {
        'documents': ['pdf', 'doc', 'docx', 'txt', 'md'],
        'images': ['jpg', 'jpeg', 'png', 'gif', 'webp'],
        'templates': ['json', 'yaml', 'yml', 'txt']
    }

    # Pagination settings
    ITEMS_PER_PAGE = 20
    SEARCH_RESULTS_PER_PAGE = 15

    # Cache settings
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes

    # Email settings (for magic links via Supabase)
    SMTP_HOST = os.environ.get('SMTP_HOST')
    SMTP_PORT = os.environ.get('SMTP_PORT', 587)
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASS = os.environ.get('SMTP_PASS')
    SMTP_FROM = os.environ.get('SMTP_FROM', 'noreply@knowledgebase.com')

    # Application settings
    APP_NAME = 'Knowledge Base'
    APP_VERSION = '1.0.0'
    APP_DESCRIPTION = 'Centralized knowledge management for development teams'

    # Feature flags
    ENABLE_API = True
    ENABLE_VERSIONING = True
    ENABLE_EXPORTS = True
    ENABLE_SOCIAL_AUTH = True

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    TESTING = False

    # Use local Supabase instance if available
    if os.environ.get('LOCAL_SUPABASE'):
        SUPABASE_URL = 'http://localhost:54321'
        DATABASE_URL = 'postgresql://postgres:postgres@localhost:54322/postgres'
        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    # Development-specific settings
    SQLALCHEMY_ECHO = True  # Log all SQL statements
    WTF_CSRF_ENABLED = False  # Disable CSRF for easier testing
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
    CREATE_TABLES_ON_START = True  # Auto-create tables in development

    # Cache settings for development
    CACHE_TYPE = 'simple'
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Disable static file caching


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    DEBUG = True

    # Use in-memory SQLite for tests
    DATABASE_URL = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    # Testing-specific settings
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True
    CREATE_TABLES_ON_START = True

    # Disable cache in tests
    CACHE_TYPE = 'null'


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False

    # Production-specific settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_NAME = 'kb_session'
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)

    # Performance settings
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_MAX_OVERFLOW = 20

    # Cache settings for production
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes

    # Logging for production
    LOG_LEVEL = 'WARNING'
    ERROR_LOG_FILE = '/tmp/error.log'

    def __init__(self):
        """Validate production configuration on instantiation."""
        super().__init__()

        # Ensure critical environment variables are set
        if not self.SECRET_KEY or self.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError('SECRET_KEY must be set in production')

        if not self.SUPABASE_URL or not self.SUPABASE_ANON_KEY:
            raise ValueError('Supabase configuration must be set in production')

        if not self.DATABASE_URL:
            raise ValueError('DATABASE_URL must be set in production')

        # Set cache configuration based on available services
        if os.environ.get('KV_REST_API_URL'):
            self.CACHE_TYPE = 'redis'
            self.CACHE_REDIS_URL = os.environ.get('KV_REST_API_URL')
            self.CACHE_DEFAULT_TIMEOUT = 3600  # 1 hour


class VercelConfig(ProductionConfig):
    """Vercel-specific production configuration."""

    def __init__(self):
        """Initialize Vercel configuration."""
        super().__init__()

        # Vercel environment detection
        self.IS_VERCEL = os.environ.get('VERCEL_ENV') is not None
        self.VERCEL_ENV = os.environ.get('VERCEL_ENV', 'development')
        self.VERCEL_URL = os.environ.get('VERCEL_URL')

        # Adjust settings for Vercel serverless environment
        if self.IS_VERCEL:
            # Use Vercel URL if available
            if self.VERCEL_URL:
                self.SERVER_NAME = self.VERCEL_URL

            # Disable SQLAlchemy event system (not needed in serverless)
            self.SQLALCHEMY_TRACK_MODIFICATIONS = False

            # Adjust pool settings for serverless
            self.SQLALCHEMY_POOL_SIZE = 1
            self.SQLALCHEMY_MAX_OVERFLOW = 0
            self.SQLALCHEMY_POOL_RECYCLE = 10

            # Use edge caching
            self.CACHE_TYPE = 'simple'  # In-memory cache per function instance
            self.CACHE_DEFAULT_TIMEOUT = 60  # Short cache for serverless


# Configuration dictionary for easy access
config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'vercel': VercelConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration object by name."""
    if config_name is None:
        # Auto-detect environment
        if os.environ.get('VERCEL_ENV'):
            config_name = 'vercel'
        elif os.environ.get('FLASK_ENV') == 'production':
            config_name = 'production'
        elif os.environ.get('TESTING'):
            config_name = 'testing'
        else:
            config_name = 'development'

    return config_dict.get(config_name, DevelopmentConfig)