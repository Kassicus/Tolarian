"""
Custom Jinja2 template filters for the Knowledge Base application.
"""

from datetime import datetime
from typing import Optional
import markdown
import bleach
from slugify import slugify as python_slugify
from markupsafe import Markup


def markdown_filter(text: str, safe: bool = True) -> str:
    """
    Convert markdown text to HTML.

    Args:
        text: Markdown text to convert
        safe: Whether to sanitize HTML output

    Returns:
        HTML string (marked as safe for Jinja2)
    """
    if not text:
        return ''

    # Configure markdown extensions
    md = markdown.Markdown(extensions=[
        'markdown.extensions.fenced_code',  # Fenced code blocks with language support
        'markdown.extensions.tables',  # Tables
        'markdown.extensions.footnotes',  # Footnotes
        'markdown.extensions.abbr',  # Abbreviations
        'markdown.extensions.def_list',  # Definition lists
        'markdown.extensions.toc',  # Table of contents
        'markdown.extensions.meta',  # Metadata
        'markdown.extensions.nl2br',  # Newline to break
        'markdown.extensions.sane_lists',  # Better list handling
    ])

    html = md.convert(text)

    # Debug: log if code blocks are present
    if '<code class="language-' in html:
        print(f"[DEBUG] Markdown filter: Found code blocks in output")
        print(f"[DEBUG] HTML preview: {html[:200]}...")

    if safe:
        # Sanitize HTML to prevent XSS
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br',
            'span', 'div', 'table', 'thead', 'tbody', 'tr', 'td', 'th',
            'del', 'ins', 'sup', 'sub', 'hr', 'img', 'kbd', 'mark'
        ]

        allowed_attributes = {
            'a': ['href', 'title', 'target', 'rel'],
            'abbr': ['title'],
            'acronym': ['title'],
            'blockquote': ['cite'],
            'code': ['class'],
            'div': ['class', 'id'],
            'span': ['class', 'id'],
            'h1': ['id'], 'h2': ['id'], 'h3': ['id'],
            'h4': ['id'], 'h5': ['id'], 'h6': ['id'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            'pre': ['class'],
            'table': ['class'],
            'td': ['align', 'colspan', 'rowspan'],
            'th': ['align', 'colspan', 'rowspan']
        }

        html = bleach.clean(
            html,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )

    return Markup(html)


def datetime_filter(dt: Optional[datetime], format: str = '%Y-%m-%d %H:%M') -> str:
    """
    Format datetime object to string.

    Args:
        dt: Datetime object to format
        format: strftime format string

    Returns:
        Formatted datetime string
    """
    if not dt:
        return ''

    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except (ValueError, AttributeError):
            return dt

    return dt.strftime(format)


def slugify_filter(text: str, max_length: int = 100) -> str:
    """
    Convert text to URL-safe slug.

    Args:
        text: Text to slugify
        max_length: Maximum length of slug

    Returns:
        URL-safe slug string
    """
    if not text:
        return ''

    return python_slugify(text, max_length=max_length)


def timesince_filter(dt: Optional[datetime]) -> str:
    """
    Get human-readable time since given datetime.

    Args:
        dt: Datetime to compare with now

    Returns:
        Human-readable time string (e.g., "2 hours ago")
    """
    if not dt:
        return ''

    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except (ValueError, AttributeError):
            return ''

    now = datetime.utcnow()
    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 60:
        return 'just now'
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours} hour{"s" if hours != 1 else ""} ago'
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f'{days} day{"s" if days != 1 else ""} ago'
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f'{weeks} week{"s" if weeks != 1 else ""} ago'
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f'{months} month{"s" if months != 1 else ""} ago'
    else:
        years = int(seconds / 31536000)
        return f'{years} year{"s" if years != 1 else ""} ago'


def filesize_filter(size: int) -> str:
    """
    Convert file size in bytes to human-readable format.

    Args:
        size: File size in bytes

    Returns:
        Human-readable file size string
    """
    if not size:
        return '0 B'

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f'{size:.1f} {unit}'
        size /= 1024.0

    return f'{size:.1f} PB'


def truncate_filter(text: str, length: int = 100, ellipsis: str = '...') -> str:
    """
    Truncate text to specified length.

    Args:
        text: Text to truncate
        length: Maximum length
        ellipsis: String to append when truncated

    Returns:
        Truncated text
    """
    if not text:
        return ''

    if len(text) <= length:
        return text

    return text[:length - len(ellipsis)].rsplit(' ', 1)[0] + ellipsis


def highlight_filter(text: str, query: str) -> str:
    """
    Highlight search query in text.

    Args:
        text: Text to highlight in
        query: Search query to highlight

    Returns:
        Text with highlighted query wrapped in <mark> tags
    """
    if not text or not query:
        return text

    import re
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    highlighted = pattern.sub(lambda m: f'<mark>{m.group()}</mark>', text)

    return Markup(highlighted)