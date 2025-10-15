"""
User API endpoints.
"""

from flask import request
from flask_login import current_user

from app.api import api_bp
from app.utils.responses import (
    success_response,
    error_response,
    not_found_response,
    forbidden_response,
    paginated_response,
    unauthorized_response
)
from app.models import User, Content
from app import db_session
from sqlalchemy import func


@api_bp.route('/users', methods=['GET'])
def list_users():
    """
    List all users (admin only).

    Query params:
    - page: Page number
    - per_page: Items per page
    """
    if not current_user.is_authenticated or current_user.role != 'admin':
        return forbidden_response("Admin access required")

    if not db_session:
        return error_response("Database not configured", status_code=500)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = db_session.query(User)
    total = query.count()
    users = query.limit(per_page).offset((page - 1) * per_page).all()

    items = [
        {
            "id": str(user.id),
            "email": user.email,
            "role": user.role.value if user.role else None,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        for user in users
    ]

    return paginated_response(
        items=items,
        page=page,
        per_page=per_page,
        total=total
    )


@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details."""
    if not current_user.is_authenticated:
        return unauthorized_response("Authentication required")

    # Users can view their own profile, admins can view any
    if current_user.id != user_id and current_user.role != 'admin':
        return forbidden_response("You don't have permission to view this profile")

    if not db_session:
        return error_response("Database not configured", status_code=500)

    user = db_session.query(User).get(user_id)
    if not user:
        return not_found_response("User")

    # Get user's content count
    content_count = db_session.query(Content).filter_by(author_id=user.id).count()

    return success_response(
        data={
            "id": str(user.id),
            "email": user.email,
            "role": user.role.value if user.role else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "content_count": content_count
        }
    )


@api_bp.route('/users/<int:user_id>/content', methods=['GET'])
def get_user_content(user_id):
    """
    Get content created by a specific user.

    Query params:
    - page: Page number
    - per_page: Items per page
    """
    if not db_session:
        return error_response("Database not configured", status_code=500)

    user = db_session.query(User).get(user_id)
    if not user:
        return not_found_response("User")

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = db_session.query(Content).filter_by(author_id=user_id).order_by(
        Content.created_at.desc()
    )
    total = query.count()
    content_items = query.limit(per_page).offset((page - 1) * per_page).all()

    items = [
        {
            "id": str(item.id),
            "title": item.title,
            "slug": item.slug,
            "category": item.category.name if item.category else None,
            "excerpt": item.body[:200] + "..." if item.body and len(item.body) > 200 else item.body,
            "tags": [tag.name for tag in item.tags] if item.tags else [],
            "created_at": item.created_at.isoformat() if item.created_at else None,
            "updated_at": item.updated_at.isoformat() if item.updated_at else None
        }
        for item in content_items
    ]

    return paginated_response(
        items=items,
        page=page,
        per_page=per_page,
        total=total
    )


@api_bp.route('/users/stats', methods=['GET'])
def get_user_stats():
    """Get user statistics (admin only)."""
    if not current_user.is_authenticated or current_user.role != 'admin':
        return forbidden_response("Admin access required")

    if not db_session:
        return error_response("Database not configured", status_code=500)

    from app.models.user import UserRole

    total_users = db_session.query(User).count()
    admin_count = db_session.query(User).filter_by(role=UserRole.ADMIN).count()
    user_count = db_session.query(User).filter_by(role=UserRole.VIEWER).count()
    editor_count = db_session.query(User).filter_by(role=UserRole.EDITOR).count()

    # Get users with most content
    top_contributors = db_session.query(
        User.id,
        User.email,
        func.count(Content.id).label('content_count')
    ).join(Content, Content.author_id == User.id).group_by(
        User.id, User.email
    ).order_by(func.count(Content.id).desc()).limit(5).all()

    return success_response(
        data={
            "total_users": total_users,
            "admin_count": admin_count,
            "viewer_count": user_count,
            "editor_count": editor_count,
            "top_contributors": [
                {
                    "id": str(contrib.id),
                    "email": contrib.email,
                    "content_count": contrib.content_count
                }
                for contrib in top_contributors
            ]
        }
    )