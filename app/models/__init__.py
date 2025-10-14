"""
Database models for the Knowledge Base application.
Uses SQLAlchemy with Supabase PostgreSQL.
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Create base class for declarative models
Base = declarative_base()

# Import all models to register them with Base
from .user import User
from .content import Content, Category, Tag, ContentTag, Version
from .search import SearchIndex

# Export all models
__all__ = [
    'Base',
    'User',
    'Content',
    'Category',
    'Tag',
    'ContentTag',
    'Version',
    'SearchIndex',
    'create_all_tables',
    'drop_all_tables'
]


def create_all_tables(engine):
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def drop_all_tables(engine):
    """Drop all database tables. Use with caution!"""
    Base.metadata.drop_all(bind=engine)