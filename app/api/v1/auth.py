"""
Authentication API endpoints.
"""

from flask import request, session, current_app
from flask_login import login_user, logout_user, current_user

from app.api import api_bp
from app.utils.responses import (
    success_response,
    error_response,
    validation_error_response,
    unauthorized_response
)
from app.models import User
from app.models.user import UserRole
from app import db_session


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """
    Login endpoint.

    Expected JSON:
    {
        "email": "user@example.com",
        "password": "password",
        "remember": true
    }
    """
    data = request.get_json()

    if not data:
        return validation_error_response({"general": "No data provided"})

    email = data.get('email')
    password = data.get('password')
    remember = data.get('remember', False)

    # Validate input
    errors = {}
    if not email:
        errors['email'] = 'Email is required'
    if not password:
        errors['password'] = 'Password is required'

    if errors:
        return validation_error_response(errors)

    # Find user
    if db_session:
        user = db_session.query(User).filter_by(email=email.lower()).first()
    else:
        return error_response("Database not configured", status_code=500)

    if not user or not user.check_password(password):
        return unauthorized_response("Invalid email or password")

    # Log in user
    login_user(user, remember=remember)

    return success_response(
        data={
            "user": {
                "id": str(user.id),
                "email": user.email,
                "role": user.role.value if user.role else None,
                "created_at": user.created_at.isoformat() if user.created_at else None
            },
            "session_id": session.get('_id')
        },
        message="Login successful"
    )


@api_bp.route('/auth/logout', methods=['POST'])
def logout():
    """Logout endpoint."""
    logout_user()
    return success_response(message="Logout successful")


@api_bp.route('/auth/register', methods=['POST'])
def register():
    """
    User registration endpoint.

    Expected JSON:
    {
        "email": "user@example.com",
        "password": "password",
        "password_confirm": "password"
    }
    """
    data = request.get_json()

    if not data:
        return validation_error_response({"general": "No data provided"})

    email = data.get('email')
    password = data.get('password')
    password_confirm = data.get('password_confirm')

    # Validate input
    errors = {}
    if not email:
        errors['email'] = 'Email is required'
    elif '@' not in email:
        errors['email'] = 'Invalid email address'

    if not password:
        errors['password'] = 'Password is required'
    elif len(password) < 8:
        errors['password'] = 'Password must be at least 8 characters'

    if password != password_confirm:
        errors['password_confirm'] = 'Passwords do not match'

    # Check if user exists
    if not db_session:
        return error_response("Database not configured", status_code=500)

    if email and db_session.query(User).filter_by(email=email.lower()).first():
        errors['email'] = 'Email already registered'

    if errors:
        return validation_error_response(errors)

    # Create new user
    try:
        user = User(
            email=email.lower()
        )
        user.set_password(password)  # Use the User model's method
        user.role = UserRole.EDITOR  # Default role for new users
        db_session.add(user)
        db_session.commit()

        # Auto login
        login_user(user)

        return success_response(
            data={
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "role": user.role.value if user.role else None,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
            },
            message="Registration successful",
            status_code=201
        )
    except Exception as e:
        db_session.rollback()
        return error_response(
            message="Registration failed",
            status_code=500,
            error_details=str(e) if current_app.debug else None
        )


@api_bp.route('/auth/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated."""
    if current_user.is_authenticated:
        return success_response(
            data={
                "authenticated": True,
                "user": {
                    "id": current_user.id,
                    "email": current_user.email,
                    "role": current_user.role
                }
            }
        )
    else:
        return success_response(
            data={"authenticated": False}
        )


@api_bp.route('/auth/profile', methods=['GET'])
def get_profile():
    """Get current user profile."""
    if not current_user.is_authenticated:
        return unauthorized_response("Not authenticated")

    return success_response(
        data={
            "id": str(current_user.id),
            "email": current_user.email,
            "role": current_user.role.value if current_user.role else None,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None
        }
    )


@api_bp.route('/auth/profile', methods=['PUT'])
def update_profile():
    """Update current user profile."""
    if not current_user.is_authenticated:
        return unauthorized_response("Not authenticated")

    data = request.get_json()
    if not data:
        return validation_error_response({"general": "No data provided"})

    if not db_session:
        return error_response("Database not configured", status_code=500)

    # Update allowed fields
    if 'email' in data:
        new_email = data['email'].lower()
        # Check if email is taken
        existing = db_session.query(User).filter_by(email=new_email).first()
        if existing and existing.id != current_user.id:
            return validation_error_response({"email": "Email already taken"})
        current_user.email = new_email

    if 'password' in data:
        if len(data['password']) < 8:
            return validation_error_response({"password": "Password must be at least 8 characters"})
        current_user.set_password(data['password'])

    try:
        db_session.commit()
        return success_response(
            data={
                "id": str(current_user.id),
                "email": current_user.email,
                "role": current_user.role.value if current_user.role else None
            },
            message="Profile updated successfully"
        )
    except Exception as e:
        db_session.rollback()
        return error_response(
            message="Failed to update profile",
            status_code=500
        )