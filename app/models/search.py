"""
Search-related models for the Knowledge Base application.
Handles search indexing and optimization.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
import uuid

from . import Base


class SearchIndex(Base):
    """
    Search index model for optimized full-text search.
    This table can be used for caching search vectors and rankings.
    """
    __tablename__ = 'search_index'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey('content.id'), nullable=False, unique=True)
    search_vector = Column(TSVECTOR, nullable=False)
    rank = Column(Float, default=0.0)  # Pre-calculated relevance score
    keywords = Column(Text, nullable=True)  # Extracted keywords
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SearchIndex {self.content_id}>'