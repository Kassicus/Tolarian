"""
User model for authentication and authorization.
For development: Uses local users table with password authentication.
For production: Will integrate with Active Directory.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
import uuid
import enum
import bcrypt

from . import Base


class UserRole(enum.Enum):
    """User role enumeration."""
    VIEWER = 'viewer'
    EDITOR = 'editor'
    ADMIN = 'admin'


class User(Base, UserMixin):
    """
    User model representing authenticated users.
    Syncs with Supabase Auth users.
    """
    __tablename__ = 'users'

    # Primary key - matches Supabase Auth user ID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic user information
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=True, index=True)
    full_name = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=True)  # For local dev only, AD in production

    # Role and permissions
    role = Column(Enum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Profile information
    avatar_url = Column(String(500), nullable=True)
    bio = Column(String(500), nullable=True)
    location = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    # Supabase Auth metadata (stored as JSON in Supabase)
    # This is handled by Supabase Auth, not stored in our users table

    def __repr__(self):
        return f'<User {self.email}>'

    def __str__(self):
        return self.email

    # Flask-Login required methods
    def get_id(self):
        """Return user ID as string for Flask-Login."""
        return str(self.id)

    @property
    def is_authenticated(self):
        """Check if user is authenticated."""
        return True

    @property
    def is_anonymous(self):
        """Check if user is anonymous."""
        return False

    def is_admin(self):
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN

    def is_editor(self):
        """Check if user has editor role or higher."""
        return self.role in [UserRole.EDITOR, UserRole.ADMIN]

    def set_password(self, password):
        """Hash and set password (for development only)."""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """Verify password against hash (for development only)."""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def can_edit(self, content=None):
        """
        Check if user can edit content.

        Args:
            content: Content object to check permissions for

        Returns:
            Boolean indicating edit permission
        """
        if self.is_admin():
            return True

        if self.is_editor():
            # Editors can edit their own content and create new content
            if content is None:
                return True
            return content.author_id == self.id

        return False

    def can_delete(self, content=None):
        """
        Check if user can delete content.

        Args:
            content: Content object to check permissions for

        Returns:
            Boolean indicating delete permission
        """
        if self.is_admin():
            return True

        if content and self.is_editor():
            return content.author_id == self.id

        return False

    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': str(self.id),
            'email': self.email,
            'username': self.username,
            'full_name': self.full_name,
            'role': self.role.value if self.role else None,
            'is_active': self.is_active,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'location': self.location,
            'website': self.website,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }

    @classmethod
    def from_supabase_user(cls, supabase_user):
        """
        Create or update User instance from Supabase Auth user data.

        Args:
            supabase_user: User data from Supabase Auth

        Returns:
            User instance
        """
        user_metadata = supabase_user.get('user_metadata', {})

        user = cls(
            id=supabase_user.get('id'),
            email=supabase_user.get('email'),
            username=user_metadata.get('username'),
            full_name=user_metadata.get('full_name'),
            avatar_url=user_metadata.get('avatar_url'),
            created_at=datetime.fromisoformat(supabase_user.get('created_at'))
            if supabase_user.get('created_at') else datetime.utcnow()
        )

        # Set role from metadata or default
        role_str = user_metadata.get('role', 'viewer')
        try:
            user.role = UserRole(role_str)
        except ValueError:
            user.role = UserRole.VIEWER

        return user