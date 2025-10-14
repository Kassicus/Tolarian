"""
Supabase client initialization and utility functions.
Provides centralized access to Supabase services.
"""

import os
from functools import lru_cache
from typing import Optional, Dict, Any, List
from supabase import create_client, Client
from flask import current_app, g
import logging

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """
    Get or create a Supabase client instance.
    Uses Flask's application context if available, otherwise falls back to env vars.

    Returns:
        Client: Supabase client instance
    """
    try:
        # Try to get from Flask app config first
        if current_app:
            url = current_app.config.get('SUPABASE_URL')
            key = current_app.config.get('SUPABASE_ANON_KEY')
        else:
            # Fallback to environment variables
            url = os.environ.get('SUPABASE_URL')
            key = os.environ.get('SUPABASE_ANON_KEY')

        if not url or not key:
            raise ValueError("Supabase URL and ANON_KEY must be configured")

        return create_client(url, key)
    except Exception as e:
        logger.error(f"Failed to create Supabase client: {e}")
        raise


@lru_cache(maxsize=1)
def get_supabase_admin_client() -> Client:
    """
    Get or create a Supabase client with service role (admin) privileges.
    Use with caution - this bypasses Row Level Security.

    Returns:
        Client: Supabase admin client instance
    """
    try:
        # Try to get from Flask app config first
        if current_app:
            url = current_app.config.get('SUPABASE_URL')
            key = current_app.config.get('SUPABASE_SERVICE_KEY')
        else:
            # Fallback to environment variables
            url = os.environ.get('SUPABASE_URL')
            key = os.environ.get('SUPABASE_SERVICE_KEY')

        if not url or not key:
            raise ValueError("Supabase URL and SERVICE_KEY must be configured for admin access")

        return create_client(url, key)
    except Exception as e:
        logger.error(f"Failed to create Supabase admin client: {e}")
        raise


def get_client() -> Client:
    """
    Get Supabase client from Flask g object or create new one.
    This ensures we reuse the same client within a request context.

    Returns:
        Client: Supabase client instance
    """
    if 'supabase_client' not in g:
        g.supabase_client = get_supabase_client()
    return g.supabase_client


class SupabaseAuthHelper:
    """Helper class for Supabase authentication operations."""

    def __init__(self, client: Optional[Client] = None):
        self.client = client or get_client()

    def sign_up(self, email: str, password: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Sign up a new user with email and password.

        Args:
            email: User's email address
            password: User's password
            metadata: Additional user metadata

        Returns:
            Dict containing user info and session
        """
        try:
            options = {"data": metadata} if metadata else {}
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": options
            })
            return response.dict() if hasattr(response, 'dict') else response
        except Exception as e:
            logger.error(f"Sign up failed: {e}")
            raise

    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """
        Sign in user with email and password.

        Args:
            email: User's email address
            password: User's password

        Returns:
            Dict containing user info and session
        """
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return response.dict() if hasattr(response, 'dict') else response
        except Exception as e:
            logger.error(f"Sign in failed: {e}")
            raise

    def sign_in_with_oauth(self, provider: str) -> Dict[str, Any]:
        """
        Initialize OAuth sign in flow.

        Args:
            provider: OAuth provider (google, github, etc.)

        Returns:
            Dict containing OAuth URL
        """
        try:
            response = self.client.auth.sign_in_with_oauth({
                "provider": provider
            })
            return response.dict() if hasattr(response, 'dict') else response
        except Exception as e:
            logger.error(f"OAuth sign in failed: {e}")
            raise

    def send_magic_link(self, email: str) -> Dict[str, Any]:
        """
        Send magic link to user's email for passwordless sign in.

        Args:
            email: User's email address

        Returns:
            Dict with success status
        """
        try:
            response = self.client.auth.sign_in_with_otp({
                "email": email
            })
            return response.dict() if hasattr(response, 'dict') else response
        except Exception as e:
            logger.error(f"Magic link send failed: {e}")
            raise

    def sign_out(self) -> bool:
        """
        Sign out current user.

        Returns:
            True if successful
        """
        try:
            self.client.auth.sign_out()
            return True
        except Exception as e:
            logger.error(f"Sign out failed: {e}")
            return False

    def get_user(self) -> Optional[Dict[str, Any]]:
        """
        Get current authenticated user.

        Returns:
            User dict or None if not authenticated
        """
        try:
            response = self.client.auth.get_user()
            if response and hasattr(response, 'user'):
                return response.user
            return None
        except Exception as e:
            logger.debug(f"No authenticated user: {e}")
            return None

    def refresh_session(self) -> Optional[Dict[str, Any]]:
        """
        Refresh current session.

        Returns:
            New session dict or None
        """
        try:
            response = self.client.auth.refresh_session()
            return response.dict() if hasattr(response, 'dict') else response
        except Exception as e:
            logger.error(f"Session refresh failed: {e}")
            return None


class SupabaseStorageHelper:
    """Helper class for Supabase storage operations."""

    def __init__(self, client: Optional[Client] = None):
        self.client = client or get_client()

    def upload_file(self, bucket: str, path: str, file_data: bytes,
                   content_type: str = None) -> Dict[str, Any]:
        """
        Upload file to Supabase storage.

        Args:
            bucket: Storage bucket name
            path: File path in bucket
            file_data: File content as bytes
            content_type: MIME type of file

        Returns:
            Dict with file info
        """
        try:
            options = {"content-type": content_type} if content_type else {}
            response = self.client.storage.from_(bucket).upload(
                path,
                file_data,
                file_options=options
            )
            return response
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            raise

    def download_file(self, bucket: str, path: str) -> bytes:
        """
        Download file from Supabase storage.

        Args:
            bucket: Storage bucket name
            path: File path in bucket

        Returns:
            File content as bytes
        """
        try:
            response = self.client.storage.from_(bucket).download(path)
            return response
        except Exception as e:
            logger.error(f"File download failed: {e}")
            raise

    def delete_file(self, bucket: str, paths: List[str]) -> bool:
        """
        Delete file(s) from Supabase storage.

        Args:
            bucket: Storage bucket name
            paths: List of file paths to delete

        Returns:
            True if successful
        """
        try:
            self.client.storage.from_(bucket).remove(paths)
            return True
        except Exception as e:
            logger.error(f"File deletion failed: {e}")
            return False

    def get_public_url(self, bucket: str, path: str) -> str:
        """
        Get public URL for a file.

        Args:
            bucket: Storage bucket name
            path: File path in bucket

        Returns:
            Public URL string
        """
        try:
            response = self.client.storage.from_(bucket).get_public_url(path)
            return response
        except Exception as e:
            logger.error(f"Failed to get public URL: {e}")
            raise

    def create_signed_url(self, bucket: str, path: str, expires_in: int = 3600) -> str:
        """
        Create signed URL for temporary file access.

        Args:
            bucket: Storage bucket name
            path: File path in bucket
            expires_in: URL expiration time in seconds

        Returns:
            Signed URL string
        """
        try:
            response = self.client.storage.from_(bucket).create_signed_url(
                path,
                expires_in
            )
            return response.get('signedURL') if isinstance(response, dict) else response
        except Exception as e:
            logger.error(f"Failed to create signed URL: {e}")
            raise

    def list_files(self, bucket: str, path: str = '', limit: int = 100) -> List[Dict[str, Any]]:
        """
        List files in a bucket/path.

        Args:
            bucket: Storage bucket name
            path: Directory path in bucket
            limit: Maximum number of files to return

        Returns:
            List of file dictionaries
        """
        try:
            response = self.client.storage.from_(bucket).list(
                path=path,
                options={"limit": limit}
            )
            return response
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            raise


# Convenience functions for direct use
def search_content(query: str, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Search content using Supabase full-text search.

    Args:
        query: Search query string
        limit: Maximum results to return
        offset: Results offset for pagination

    Returns:
        List of search results
    """
    client = get_client()
    try:
        response = client.rpc('search_content', {
            'search_query': query,
            'result_limit': limit,
            'result_offset': offset
        }).execute()
        return response.data if response else []
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []


def get_search_suggestions(partial_query: str, limit: int = 5) -> List[str]:
    """
    Get search suggestions based on partial query.

    Args:
        partial_query: Partial search query
        limit: Maximum suggestions to return

    Returns:
        List of suggestion strings
    """
    client = get_client()
    try:
        response = client.rpc('search_suggestions', {
            'partial_query': partial_query,
            'suggestion_limit': limit
        }).execute()
        return [r['suggestion'] for r in response.data] if response else []
    except Exception as e:
        logger.error(f"Failed to get suggestions: {e}")
        return []