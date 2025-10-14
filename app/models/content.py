"""
Content models for the Knowledge Base application.
Includes Content, Category, Tag, and Version models.
"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Text, DateTime, Enum, Boolean,
    ForeignKey, Integer, JSON, Table, Index
)
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import relationship, backref
import uuid
import enum

from . import Base


class ContentType(enum.Enum):
    """Content type enumeration."""
    DOCUMENT = 'document'
    TEMPLATE = 'template'
    GUIDE = 'guide'
    LINK = 'link'


class ContentStatus(enum.Enum):
    """Content status enumeration."""
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'


# Many-to-Many association table for Content and Tags
content_tags = Table(
    'content_tags',
    Base.metadata,
    Column('content_id', UUID(as_uuid=True), ForeignKey('content.id', ondelete='CASCADE')),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'))
)


class Category(Base):
    """Category model for organizing content."""
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  # Bootstrap icon name
    parent_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=True)
    order_index = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    parent = relationship('Category', remote_side=[id], backref='subcategories')
    content = relationship('Content', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'

    def get_breadcrumb(self):
        """Get category breadcrumb path."""
        path = []
        current = self
        while current:
            path.insert(0, current)
            current = current.parent
        return path


class Tag(Base):
    """Tag model for content tagging."""
    __tablename__ = 'tags'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    color = Column(String(7), default='#6c757d')  # Hex color code

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    content = relationship('Content', secondary=content_tags, back_populates='tags')

    def __repr__(self):
        return f'<Tag {self.name}>'


class Content(Base):
    """Main content model for all knowledge base items."""
    __tablename__ = 'content'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content_type = Column(Enum(ContentType), nullable=False)
    body = Column(Text, nullable=True)  # Markdown content
    content_metadata = Column(JSON, nullable=True)  # Additional structured data

    # Foreign keys
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    # Status and visibility
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT, nullable=False)
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)

    # Search vector for full-text search (PostgreSQL specific)
    search_vector = Column(TSVECTOR, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)

    # Relationships
    category = relationship('Category', back_populates='content')
    author = relationship('User', backref=backref('content', lazy='dynamic'))
    tags = relationship('Tag', secondary=content_tags, back_populates='content')
    versions = relationship('Version', back_populates='content', cascade='all, delete-orphan',
                          order_by='desc(Version.version_number)')

    # Indexes for better performance
    __table_args__ = (
        Index('idx_content_status', 'status'),
        Index('idx_content_type', 'content_type'),
        Index('idx_content_author', 'author_id'),
        Index('idx_content_category', 'category_id'),
        Index('idx_content_search', 'search_vector', postgresql_using='gin'),
    )

    def __repr__(self):
        return f'<Content {self.title}>'

    def get_excerpt(self, length=200):
        """Get excerpt from content body."""
        if not self.body:
            return ''
        # Strip markdown and return first N characters
        import re
        text = re.sub(r'[#*`\[\]()]', '', self.body)
        return text[:length] + '...' if len(text) > length else text

    def increment_view_count(self):
        """Increment view counter."""
        self.view_count = (self.view_count or 0) + 1

    def publish(self):
        """Publish content."""
        self.status = ContentStatus.PUBLISHED
        self.published_at = datetime.utcnow()

    def archive(self):
        """Archive content."""
        self.status = ContentStatus.ARCHIVED

    def to_dict(self):
        """Convert content to dictionary."""
        return {
            'id': str(self.id),
            'title': self.title,
            'slug': self.slug,
            'content_type': self.content_type.value if self.content_type else None,
            'body': self.body,
            'metadata': self.content_metadata,
            'category': self.category.name if self.category else None,
            'author_id': str(self.author_id),
            'status': self.status.value if self.status else None,
            'is_featured': self.is_featured,
            'view_count': self.view_count,
            'tags': [tag.name for tag in self.tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }


class ContentTag(Base):
    """Association model for Content and Tags (if needed for additional fields)."""
    __tablename__ = 'content_tags_extra'

    content_id = Column(UUID(as_uuid=True), ForeignKey('content.id'), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    added_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)


class Version(Base):
    """Version model for content version control."""
    __tablename__ = 'versions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey('content.id'), nullable=False)
    version_number = Column(Integer, nullable=False)
    changes = Column(JSON, nullable=True)  # Diff or full content snapshot
    commit_message = Column(String(255), nullable=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    content = relationship('Content', back_populates='versions')
    author = relationship('User', backref='versions')

    # Unique constraint on content_id and version_number
    __table_args__ = (
        Index('idx_version_content', 'content_id', 'version_number', unique=True),
    )

    def __repr__(self):
        return f'<Version {self.content_id}:{self.version_number}>'