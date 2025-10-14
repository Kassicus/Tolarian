"""
Content forms for creating and editing knowledge base content.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, HiddenField, FieldList
from wtforms.validators import DataRequired, Length, Optional, URL, ValidationError
from wtforms.widgets import TextArea
import re


class SlugField(StringField):
    """Custom field for URL slugs."""

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.slugify(valuelist[0])
        else:
            self.data = ''

    @staticmethod
    def slugify(text):
        """Convert text to URL-friendly slug."""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')


class ContentForm(FlaskForm):
    """Form for creating/editing content."""

    title = StringField('Title',
                       validators=[DataRequired(), Length(min=3, max=255)],
                       render_kw={'class': 'form-control', 'placeholder': 'Enter a descriptive title'})

    slug = SlugField('URL Slug',
                    validators=[Optional(), Length(max=255)],
                    render_kw={'class': 'form-control', 'placeholder': 'auto-generated-from-title'})

    content_type = SelectField('Content Type',
                             choices=[
                                 ('document', 'Document'),
                                 ('template', 'Template'),
                                 ('guide', 'Guide'),
                                 ('link', 'External Link')
                             ],
                             validators=[DataRequired()],
                             render_kw={'class': 'form-select'})

    category_id = SelectField('Category',
                             choices=[],  # Will be populated dynamically
                             validators=[Optional()],
                             coerce=str,
                             render_kw={'class': 'form-select'})

    body = TextAreaField('Content',
                        validators=[Optional()],
                        widget=TextArea(),
                        render_kw={'class': 'form-control', 'rows': 15,
                                 'placeholder': 'Write your content in Markdown...'})

    external_url = StringField('External URL',
                              validators=[Optional(), URL()],
                              render_kw={'class': 'form-control',
                                       'placeholder': 'https://example.com/resource'})

    tags = StringField('Tags',
                      validators=[Optional()],
                      render_kw={'class': 'form-control',
                               'placeholder': 'python, flask, tutorial (comma-separated)'})

    is_featured = BooleanField('Featured Content',
                              render_kw={'class': 'form-check-input'})

    status = SelectField('Status',
                        choices=[
                            ('draft', 'Draft'),
                            ('published', 'Published'),
                            ('archived', 'Archived')
                        ],
                        default='draft',
                        render_kw={'class': 'form-select'})

    def validate_body(self, field):
        """Validate body content based on content type."""
        if self.content_type.data != 'link' and not field.data:
            raise ValidationError('Content is required for documents, templates, and guides.')

    def validate_external_url(self, field):
        """Validate external URL for link type."""
        if self.content_type.data == 'link' and not field.data:
            raise ValidationError('External URL is required for link content type.')

    def validate_slug(self, field):
        """Auto-generate slug from title if not provided."""
        if not field.data and self.title.data:
            field.data = SlugField.slugify(self.title.data)


class SearchForm(FlaskForm):
    """Form for searching content."""

    q = StringField('Search',
                   validators=[Optional(), Length(max=200)],
                   render_kw={'class': 'form-control',
                            'placeholder': 'Search documentation...'})

    content_type = SelectField('Type',
                             choices=[
                                 ('', 'All Types'),
                                 ('document', 'Documents'),
                                 ('template', 'Templates'),
                                 ('guide', 'Guides'),
                                 ('link', 'Links')
                             ],
                             validators=[Optional()],
                             render_kw={'class': 'form-select form-select-sm'})

    category = SelectField('Category',
                         choices=[],  # Will be populated dynamically
                         validators=[Optional()],
                         render_kw={'class': 'form-select form-select-sm'})

    status = SelectField('Status',
                        choices=[
                            ('published', 'Published'),
                            ('draft', 'Draft'),
                            ('', 'All')
                        ],
                        default='published',
                        validators=[Optional()],
                        render_kw={'class': 'form-select form-select-sm'})


class CategoryForm(FlaskForm):
    """Form for creating/editing categories."""

    name = StringField('Name',
                      validators=[DataRequired(), Length(min=2, max=100)],
                      render_kw={'class': 'form-control'})

    slug = SlugField('URL Slug',
                    validators=[Optional(), Length(max=100)],
                    render_kw={'class': 'form-control'})

    description = TextAreaField('Description',
                              validators=[Optional(), Length(max=500)],
                              render_kw={'class': 'form-control', 'rows': 3})

    icon = StringField('Icon',
                      validators=[Optional(), Length(max=50)],
                      render_kw={'class': 'form-control',
                               'placeholder': 'bi-folder (Bootstrap icon class)'})

    parent_id = SelectField('Parent Category',
                          choices=[],  # Will be populated dynamically
                          validators=[Optional()],
                          coerce=str,
                          render_kw={'class': 'form-select'})

    order_index = StringField('Order',
                            validators=[Optional()],
                            default='0',
                            render_kw={'class': 'form-control', 'type': 'number'})


class TagForm(FlaskForm):
    """Form for creating/editing tags."""

    name = StringField('Name',
                      validators=[DataRequired(), Length(min=2, max=50)],
                      render_kw={'class': 'form-control'})

    slug = SlugField('URL Slug',
                    validators=[Optional(), Length(max=50)],
                    render_kw={'class': 'form-control'})

    color = StringField('Color',
                       validators=[Optional(), Length(max=7)],
                       default='#6c757d',
                       render_kw={'class': 'form-control', 'type': 'color'})