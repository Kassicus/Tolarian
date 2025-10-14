"""
Forms for the Knowledge Base application.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, URL


class LoginForm(FlaskForm):
    """Login form for local authentication."""
    username_or_email = StringField('Username or Email',
                                   validators=[DataRequired(), Length(min=3, max=255)],
                                   render_kw={"placeholder": "Enter username or email"})
    password = PasswordField('Password',
                           validators=[DataRequired()],
                           render_kw={"placeholder": "Enter password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')