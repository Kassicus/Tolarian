"""
Utility modules for the Knowledge Base application.
"""

from .supabase import (
    get_client,
    get_supabase_client,
    get_supabase_admin_client,
    SupabaseAuthHelper,
    SupabaseStorageHelper,
    search_content,
    get_search_suggestions
)

__all__ = [
    'get_client',
    'get_supabase_client',
    'get_supabase_admin_client',
    'SupabaseAuthHelper',
    'SupabaseStorageHelper',
    'search_content',
    'get_search_suggestions'
]