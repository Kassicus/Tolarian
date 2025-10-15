"""
Search API endpoints.
"""

from flask import request
from app.api import api_bp
from app.utils.responses import success_response, validation_error_response, error_response
from app.models import Content
from app import db_session
from sqlalchemy import or_


@api_bp.route('/search', methods=['GET'])
def search():
    """
    Search content.

    Query params:
    - q: Search query (required)
    - category: Filter by category
    - limit: Max results (default: 20)
    """
    query = request.args.get('q')
    category = request.args.get('category')
    limit = request.args.get('limit', 20, type=int)

    if not query:
        return validation_error_response({"query": "Search query is required"})

    # Build search query
    if not db_session:
        return error_response("Database not configured", status_code=500)

    search_term = f"%{query}%"
    db_query = db_session.query(Content).filter(
        or_(
            Content.title.ilike(search_term),
            Content.body.ilike(search_term)  # Changed from content to body
        )
    )

    # Apply category filter
    if category:
        db_query = db_query.filter_by(category=category)

    # Order by relevance (simple approach - in production use full-text search)
    db_query = db_query.order_by(Content.updated_at.desc())

    # Limit results
    results = db_query.limit(limit).all()

    # Format results
    items = []
    for item in results:
        # Extract snippet around match
        if item.body:
            content_lower = item.body.lower()
            query_lower = query.lower()
            snippet_start = max(0, content_lower.find(query_lower) - 50)
            snippet_end = min(len(item.body), snippet_start + 200)
            snippet = item.body[snippet_start:snippet_end]
        else:
            snippet = ""

        items.append({
            "id": str(item.id),
            "title": item.title,
            "slug": item.slug,
            "category": item.category.name if item.category else None,
            "snippet": f"...{snippet}..." if snippet_start > 0 else f"{snippet}...",
            "tags": [tag.name for tag in item.tags] if item.tags else [],
            "updated_at": item.updated_at.isoformat() if item.updated_at else None
        })

    return success_response(
        data={
            "query": query,
            "results": items,
            "count": len(items)
        }
    )


@api_bp.route('/search/suggestions', methods=['GET'])
def search_suggestions():
    """
    Get search suggestions based on partial query.

    Query params:
    - q: Partial search query (required)
    - limit: Max suggestions (default: 10)
    """
    query = request.args.get('q')
    limit = request.args.get('limit', 10, type=int)

    if not query or len(query) < 2:
        return success_response(data=[])

    if not db_session:
        return error_response("Database not configured", status_code=500)

    # Search for titles that start with or contain the query
    search_term = f"%{query}%"
    results = db_session.query(Content).filter(
        Content.title.ilike(search_term)
    ).order_by(Content.updated_at.desc()).limit(limit).all()

    suggestions = [
        {
            "id": str(item.id),
            "title": item.title,
            "category": item.category.name if item.category else None
        }
        for item in results
    ]

    return success_response(data=suggestions)