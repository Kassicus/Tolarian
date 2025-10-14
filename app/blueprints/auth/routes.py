"""Authentication routes."""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import or_
from . import auth_bp
from app.forms import LoginForm
from app.models import User
from app.models.user import UserRole
from app import db_session
from app.utils.supabase import get_supabase_admin_client


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route for local authentication."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Get form data
        username_or_email = form.username_or_email.data
        password = form.password.data

        # Try to find user in Supabase
        try:
            client = get_supabase_admin_client()

            # Query for user by email or username
            result = client.table('users').select('*').or_(
                f'email.eq.{username_or_email},username.eq.{username_or_email}'
            ).execute()

            if result.data and len(result.data) > 0:
                user_data = result.data[0]

                # Create User object from Supabase data
                user = User()
                user.id = user_data['id']
                user.email = user_data['email']
                user.username = user_data.get('username')
                user.full_name = user_data.get('full_name')
                user.password_hash = user_data.get('password_hash')
                user.role = UserRole(user_data.get('role', 'viewer'))
                user.is_active = user_data.get('is_active', True)
                user.avatar_url = user_data.get('avatar_url')
                user.bio = user_data.get('bio')
                user.location = user_data.get('location')
                user.website = user_data.get('website')

                # Check if user is active
                if not user.is_active:
                    flash('Your account has been disabled. Please contact an administrator.', 'warning')
                    return render_template('auth/login.html', form=form)

                # Verify password
                if user.check_password(password):
                    # Update last login time
                    from datetime import datetime
                    client.table('users').update({
                        'last_login_at': datetime.utcnow().isoformat()
                    }).eq('id', user.id).execute()

                    # Login user
                    login_user(user, remember=form.remember_me.data)

                    # Flash success message based on role
                    if user.is_admin():
                        flash(f'Welcome back, {user.full_name or user.username}! (Admin)', 'success')
                    elif user.is_editor():
                        flash(f'Welcome back, {user.full_name or user.username}! (Editor)', 'success')
                    else:
                        flash(f'Welcome back, {user.full_name or user.username}!', 'success')

                    # Redirect to next page or home
                    next_page = request.args.get('next')
                    if not next_page or not next_page.startswith('/'):
                        next_page = url_for('main.index')
                    return redirect(next_page)
                else:
                    flash('Invalid username/email or password.', 'danger')
            else:
                flash('Invalid username/email or password.', 'danger')

        except Exception as e:
            print(f"Login error: {e}")
            flash('An error occurred during login. Please try again.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout route."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('auth/profile.html')


# Remove the register route since we're using AD in production
# and seeded users for development