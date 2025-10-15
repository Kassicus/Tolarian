"""
Content API endpoints.
"""

from flask import request
from flask_login import current_user
from datetime import datetime

from app.api import api_bp
from app.utils.responses import (
    success_response,
    error_response,
    validation_error_response,
    not_found_response,
    forbidden_response,
    paginated_response,
    unauthorized_response
)
from app.models import Content, Category
from app import db_session
from sqlalchemy import or_


@api_bp.route('/content', methods=['GET'])
def list_content():
    """
    List all content with pagination and filtering.

    Query params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    - category: Filter by category
    - search: Search in title and content
    - sort: Sort by field (created_at, updated_at, title)
    - order: Sort order (asc, desc)
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    search = request.args.get('search')
    sort = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')

    # Check database session
    if not db_session:
        return error_response("Database not configured", status_code=500)

    # Start query
    query = db_session.query(Content)

    # Apply filters
    if category:
        query = query.filter_by(category=category)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Content.title.ilike(search_term),
                Content.body.ilike(search_term)
            )
        )

    # Apply sorting
    if hasattr(Content, sort):
        sort_column = getattr(Content, sort)
        if order == 'desc':
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)

    # Manual pagination since SQLAlchemy doesn't have paginate
    total = query.count()
    items = query.limit(per_page).offset((page - 1) * per_page).all()

    # Format items
    formatted_items = []
    for item in items:
        formatted_items.append({
            "id": str(item.id),
            "title": item.title,
            "slug": item.slug,
            "content_type": item.content_type.value if item.content_type else None,
            "category": item.category.name if item.category else None,
            "body": item.body[:200] + "..." if item.body and len(item.body) > 200 else item.body,
            "status": item.status.value if item.status else None,
            "is_featured": item.is_featured,
            "view_count": item.view_count,
            "tags": [tag.name for tag in item.tags] if item.tags else [],
            "author_id": str(item.author_id),
            "created_at": item.created_at.isoformat() if item.created_at else None,
            "updated_at": item.updated_at.isoformat() if item.updated_at else None,
            "published_at": item.published_at.isoformat() if item.published_at else None
        })

    return paginated_response(
        items=formatted_items,
        page=page,
        per_page=per_page,
        total=total
    )


@api_bp.route('/content/<content_id>', methods=['GET'])
def get_content(content_id):
    """Get single content item by ID."""
    if not db_session:
        return error_response("Database not configured", status_code=500)

    # Handle UUID string
    import uuid
    try:
        content_uuid = uuid.UUID(content_id)
    except ValueError:
        return error_response("Invalid content ID format", status_code=400)

    content = db_session.query(Content).filter_by(id=content_uuid).first()

    if not content:
        return not_found_response("Content")

    return success_response(
        data={
            "id": str(content.id),
            "title": content.title,
            "slug": content.slug,
            "content_type": content.content_type.value if content.content_type else None,
            "category": content.category.name if content.category else None,
            "body": content.body,
            "status": content.status.value if content.status else None,
            "is_featured": content.is_featured,
            "view_count": content.view_count,
            "tags": [tag.name for tag in content.tags] if content.tags else [],
            "author_id": str(content.author_id),
            "created_at": content.created_at.isoformat() if content.created_at else None,
            "updated_at": content.updated_at.isoformat() if content.updated_at else None,
            "published_at": content.published_at.isoformat() if content.published_at else None
        }
    )


@api_bp.route('/content', methods=['POST'])
def create_content():
    """
    Create new content.

    Expected JSON:
    {
        "title": "Content Title",
        "category": "guide",
        "content": "Content body...",
        "tags": ["tag1", "tag2"]
    }
    """
    if not current_user.is_authenticated:
        return unauthorized_response("Authentication required")

    data = request.get_json()
    if not data:
        return validation_error_response({"general": "No data provided"})

    # Validate required fields
    errors = {}
    if not data.get('title'):
        errors['title'] = 'Title is required'
    if not data.get('content'):
        errors['content'] = 'Content is required'
    if not data.get('category'):
        errors['category'] = 'Category is required'

    if errors:
        return validation_error_response(errors)

    # Create slug from title
    import re
    slug = re.sub(r'[^\w\s-]', '', data['title'].lower())
    slug = re.sub(r'[-\s]+', '-', slug)

    if not db_session:
        return error_response("Database not configured", status_code=500)

    # Check if slug exists
    existing = db_session.query(Content).filter_by(slug=slug).first()
    if existing:
        slug = f"{slug}-{int(datetime.now().timestamp())}"

    # Create content
    try:
        import uuid
        from app.models.content import ContentType, ContentStatus

        content = Content(
            id=uuid.uuid4(),
            title=data['title'],
            slug=slug,
            content_type=ContentType.DOCUMENT,  # Default type
            body=data['content'],
            author_id=current_user.id,
            status=ContentStatus.DRAFT,  # Start as draft
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        # Handle category and tags separately if needed

        db_session.add(content)
        db_session.commit()

        return success_response(
            data={
                "id": str(content.id),
                "title": content.title,
                "slug": content.slug,
                "category": content.category.name if content.category else None
            },
            message="Content created successfully",
            status_code=201
        )
    except Exception as e:
        db_session.rollback()
        return error_response(
            message="Failed to create content",
            status_code=500
        )


@api_bp.route('/content/<content_id>', methods=['PUT'])
def update_content(content_id):
    """Update existing content."""
    if not current_user.is_authenticated:
        return unauthorized_response("Authentication required")

    if not db_session:
        return error_response("Database not configured", status_code=500)

    # Handle UUID string
    import uuid
    try:
        content_uuid = uuid.UUID(content_id)
    except ValueError:
        return error_response("Invalid content ID format", status_code=400)

    content = db_session.query(Content).filter_by(id=content_uuid).first()
    if not content:
        return not_found_response("Content")

    # Check permission
    if content.author_id != current_user.id and current_user.role != 'admin':
        return forbidden_response("You don't have permission to edit this content")

    data = request.get_json()
    if not data:
        return validation_error_response({"general": "No data provided"})

    # Update fields
    if 'title' in data:
        content.title = data['title']
    if 'content' in data:
        content.body = data['content']
    # Handle category and tags updates separately if needed

    content.updated_at = datetime.utcnow()

    try:
        db_session.commit()
        return success_response(
            data={
                "id": str(content.id),
                "title": content.title,
                "slug": content.slug,
                "category": content.category.name if content.category else None
            },
            message="Content updated successfully"
        )
    except Exception as e:
        db_session.rollback()
        return error_response(
            message="Failed to update content",
            status_code=500
        )


@api_bp.route('/content/<content_id>', methods=['DELETE'])
def delete_content(content_id):
    """Delete content."""
    if not current_user.is_authenticated:
        return unauthorized_response("Authentication required")

    if not db_session:
        return error_response("Database not configured", status_code=500)

    # Handle UUID string
    import uuid
    try:
        content_uuid = uuid.UUID(content_id)
    except ValueError:
        return error_response("Invalid content ID format", status_code=400)

    content = db_session.query(Content).filter_by(id=content_uuid).first()
    if not content:
        return not_found_response("Content")

    # Check permission
    if content.author_id != current_user.id and current_user.role != 'admin':
        return forbidden_response("You don't have permission to delete this content")

    try:
        db_session.delete(content)
        db_session.commit()
        return success_response(message="Content deleted successfully")
    except Exception as e:
        db_session.rollback()
        return error_response(
            message="Failed to delete content",
            status_code=500
        )


@api_bp.route('/content/categories', methods=['GET'])
def get_categories():
    """Get list of available categories."""
    # In a real app, this might come from database
    categories = [
        {"id": "guide", "name": "Guides", "icon": "book"},
        {"id": "template", "name": "Templates", "icon": "file-earmark-text"},
        {"id": "development", "name": "Development", "icon": "code-slash"},
        {"id": "documentation", "name": "Documentation", "icon": "file-text"},
        {"id": "tutorial", "name": "Tutorials", "icon": "mortarboard"}
    ]

    return success_response(data=categories)