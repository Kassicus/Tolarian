"""
Standardized API response helpers for consistent JSON responses.
"""

from flask import jsonify
from typing import Any, Dict, Optional, List


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
    **kwargs
) -> tuple:
    """
    Create a standardized success response.

    Args:
        data: The data to return
        message: Success message
        status_code: HTTP status code
        **kwargs: Additional fields to include in response

    Returns:
        Tuple of (response, status_code)
    """
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    response.update(kwargs)
    return jsonify(response), status_code


def error_response(
    message: str = "An error occurred",
    status_code: int = 400,
    errors: Optional[Dict[str, Any]] = None,
    **kwargs
) -> tuple:
    """
    Create a standardized error response.

    Args:
        message: Error message
        status_code: HTTP status code
        errors: Dictionary of field-specific errors
        **kwargs: Additional fields to include in response

    Returns:
        Tuple of (response, status_code)
    """
    response = {
        "success": False,
        "message": message
    }

    if errors:
        response["errors"] = errors

    response.update(kwargs)
    return jsonify(response), status_code


def paginated_response(
    items: List[Any],
    page: int,
    per_page: int,
    total: int,
    message: str = "Success",
    **kwargs
) -> tuple:
    """
    Create a paginated response.

    Args:
        items: List of items for current page
        page: Current page number
        per_page: Items per page
        total: Total number of items
        message: Success message
        **kwargs: Additional fields

    Returns:
        Tuple of (response, status_code)
    """
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    response = {
        "success": True,
        "message": message,
        "data": items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
            "has_prev": page > 1,
            "has_next": page < total_pages
        }
    }
    response.update(kwargs)
    return jsonify(response), 200


def validation_error_response(errors: Dict[str, Any]) -> tuple:
    """
    Create a validation error response.

    Args:
        errors: Dictionary of validation errors

    Returns:
        Tuple of (response, status_code)
    """
    return error_response(
        message="Validation failed",
        status_code=422,
        errors=errors
    )


def not_found_response(resource: str = "Resource") -> tuple:
    """
    Create a not found response.

    Args:
        resource: Name of the resource that wasn't found

    Returns:
        Tuple of (response, status_code)
    """
    return error_response(
        message=f"{resource} not found",
        status_code=404
    )


def unauthorized_response(message: str = "Unauthorized") -> tuple:
    """
    Create an unauthorized response.

    Args:
        message: Error message

    Returns:
        Tuple of (response, status_code)
    """
    return error_response(
        message=message,
        status_code=401
    )


def forbidden_response(message: str = "Forbidden") -> tuple:
    """
    Create a forbidden response.

    Args:
        message: Error message

    Returns:
        Tuple of (response, status_code)
    """
    return error_response(
        message=message,
        status_code=403
    )