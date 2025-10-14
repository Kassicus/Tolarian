"""Content management routes."""
from flask import render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import uuid
from . import content_bp
from app.forms.content import ContentForm, CategoryForm, TagForm, SlugField
from app.utils.supabase import get_supabase_admin_client
from app.models.user import UserRole


@content_bp.route('/')
def index():
    """Content index page."""
    return redirect(url_for('content.list'))


@content_bp.route('/list')
def list():
    """List all published content."""
    try:
        client = get_supabase_admin_client()

        # Get filter parameters
        content_type = request.args.get('type')
        category_id = request.args.get('category')
        tag = request.args.get('tag')

        # Build query
        query = client.table('content').select(
            '*, categories!category_id(name, slug), users!author_id(email, full_name)'
        )

        # Apply filters
        if not current_user.is_authenticated:
            query = query.eq('status', 'published')
        elif not current_user.is_admin():
            query = query.or_(f'status.eq.published,author_id.eq.{current_user.id}')

        if content_type:
            query = query.eq('content_type', content_type)
        if category_id:
            query = query.eq('category_id', category_id)

        # Execute query
        result = query.order('created_at', desc=True).execute()
        content_list = result.data if result.data else []

        # Get categories for filter
        categories_result = client.table('categories').select('*').order('name').execute()
        categories = categories_result.data if categories_result.data else []

        return render_template('content/list.html',
                             content_list=content_list,
                             categories=categories,
                             current_type=content_type,
                             current_category=category_id)
    except Exception as e:
        flash(f'Error loading content: {str(e)}', 'danger')
        return render_template('content/list.html', content_list=[], categories=[])


@content_bp.route('/my')
@login_required
def my_content():
    """List current user's content."""
    try:
        client = get_supabase_admin_client()

        # Get user's content
        result = client.table('content').select(
            '*, categories!category_id(name, slug)'
        ).eq('author_id', current_user.id).order('updated_at', desc=True).execute()

        content_list = result.data if result.data else []

        return render_template('content/my_content.html', content_list=content_list)
    except Exception as e:
        flash(f'Error loading your content: {str(e)}', 'danger')
        return render_template('content/my_content.html', content_list=[])


@content_bp.route('/view/<string:content_id>')
def view(content_id):
    """View content detail."""
    try:
        client = get_supabase_admin_client()

        # Get content with related data
        result = client.table('content').select(
            '*, categories!category_id(name, slug, icon), users!author_id(email, full_name, avatar_url)'
        ).eq('id', content_id).single().execute()

        if not result.data:
            abort(404)

        content = result.data

        # Check access permissions
        if content['status'] != 'published':
            if not current_user.is_authenticated:
                abort(403)
            if not current_user.is_admin() and str(content['author_id']) != str(current_user.id):
                abort(403)

        # Increment view count for published content
        if content['status'] == 'published':
            client.table('content').update({
                'view_count': content.get('view_count', 0) + 1
            }).eq('id', content_id).execute()

        # Get related content (same category)
        related = []
        if content.get('category_id'):
            related_result = client.table('content').select(
                'id, title, slug, content_type'
            ).eq('category_id', content['category_id']).neq('id', content_id).eq(
                'status', 'published'
            ).limit(5).execute()
            related = related_result.data if related_result.data else []

        return render_template('content/view.html', content=content, related=related)
    except Exception as e:
        flash(f'Error loading content: {str(e)}', 'danger')
        abort(404)


@content_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new content."""
    if not current_user.is_editor():
        flash('You need editor permissions to create content.', 'warning')
        return redirect(url_for('content.list'))

    form = ContentForm()

    try:
        client = get_supabase_admin_client()

        # Populate category choices
        categories_result = client.table('categories').select('id, name').order('name').execute()
        form.category_id.choices = [('', '-- Select Category --')] + [
            (str(cat['id']), cat['name']) for cat in (categories_result.data or [])
        ]

        if form.validate_on_submit():
            # Prepare content data
            content_data = {
                'id': str(uuid.uuid4()),
                'title': form.title.data,
                'slug': form.slug.data or SlugField.slugify(form.title.data),
                'content_type': form.content_type.data,
                'body': form.body.data if form.content_type.data != 'link' else None,
                'content_metadata': {
                    'external_url': form.external_url.data if form.content_type.data == 'link' else None
                },
                'category_id': form.category_id.data if form.category_id.data else None,
                'author_id': current_user.id,
                'status': form.status.data,
                'is_featured': form.is_featured.data,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }

            if form.status.data == 'published':
                content_data['published_at'] = datetime.utcnow().isoformat()

            # Insert content
            try:
                result = client.table('content').insert(content_data).execute()
            except Exception as insert_error:
                # Check for duplicate slug error
                if '23505' in str(insert_error) or 'duplicate key' in str(insert_error).lower():
                    flash(f'A content item with the slug "{content_data["slug"]}" already exists. Please use a different title or slug.', 'danger')
                    return render_template('content/form.html', form=form, title='Create Content')
                else:
                    raise insert_error

            if result.data:
                # Handle tags
                if form.tags.data:
                    tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
                    for tag_name in tags:
                        tag_slug = SlugField.slugify(tag_name)

                        # Check if tag exists by slug (more reliable)
                        tag_result = client.table('tags').select('id').eq('slug', tag_slug).execute()
                        if tag_result.data:
                            tag_id = tag_result.data[0]['id']
                        else:
                            # Create new tag
                            try:
                                new_tag = {
                                    'id': str(uuid.uuid4()),
                                    'name': tag_name,
                                    'slug': tag_slug
                                }
                                tag_insert = client.table('tags').insert(new_tag).execute()
                                tag_id = tag_insert.data[0]['id'] if tag_insert.data else None
                            except Exception as tag_error:
                                # Tag might have been created by another request, try to fetch again
                                tag_result = client.table('tags').select('id').eq('slug', tag_slug).execute()
                                tag_id = tag_result.data[0]['id'] if tag_result.data else None

                        # Link tag to content
                        if tag_id:
                            try:
                                client.table('content_tags').insert({
                                    'content_id': content_data['id'],
                                    'tag_id': tag_id
                                }).execute()
                            except Exception:
                                # Link might already exist, ignore
                                pass

                flash('Content created successfully!', 'success')
                return redirect(url_for('content.view', content_id=content_data['id']))
            else:
                flash('Error creating content.', 'danger')

    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')

    return render_template('content/form.html', form=form, title='Create Content')


@content_bp.route('/edit/<string:content_id>', methods=['GET', 'POST'])
@login_required
def edit(content_id):
    """Edit existing content."""
    try:
        client = get_supabase_admin_client()

        # Get existing content
        result = client.table('content').select('*').eq('id', content_id).single().execute()
        if not result.data:
            abort(404)

        content = result.data

        # Check permissions
        if not current_user.is_admin() and str(content['author_id']) != str(current_user.id):
            flash('You do not have permission to edit this content.', 'danger')
            return redirect(url_for('content.view', content_id=content_id))

        form = ContentForm()

        # Populate category choices
        categories_result = client.table('categories').select('id, name').order('name').execute()
        form.category_id.choices = [('', '-- Select Category --')] + [
            (str(cat['id']), cat['name']) for cat in (categories_result.data or [])
        ]

        if form.validate_on_submit():
            # Update content
            update_data = {
                'title': form.title.data,
                'slug': form.slug.data,
                'content_type': form.content_type.data,
                'body': form.body.data if form.content_type.data != 'link' else None,
                'content_metadata': {
                    'external_url': form.external_url.data if form.content_type.data == 'link' else None
                },
                'category_id': form.category_id.data if form.category_id.data else None,
                'status': form.status.data,
                'is_featured': form.is_featured.data,
                'updated_at': datetime.utcnow().isoformat()
            }

            if form.status.data == 'published' and content.get('published_at') is None:
                update_data['published_at'] = datetime.utcnow().isoformat()

            result = client.table('content').update(update_data).eq('id', content_id).execute()

            if result.data:
                flash('Content updated successfully!', 'success')
                return redirect(url_for('content.view', content_id=content_id))
            else:
                flash('Error updating content.', 'danger')

        elif request.method == 'GET':
            # Populate form with existing data
            form.title.data = content['title']
            form.slug.data = content['slug']
            form.content_type.data = content['content_type']
            form.body.data = content.get('body', '')
            form.category_id.data = str(content['category_id']) if content.get('category_id') else ''
            form.status.data = content['status']
            form.is_featured.data = content.get('is_featured', False)

            # Handle metadata
            metadata = content.get('content_metadata', {})
            if metadata and isinstance(metadata, dict):
                form.external_url.data = metadata.get('external_url', '')

            # Get existing tags
            tags_result = client.table('content_tags').select('tags!tag_id(name)').eq('content_id', content_id).execute()
            if tags_result.data:
                tag_names = [t['tags']['name'] for t in tags_result.data if t.get('tags')]
                form.tags.data = ', '.join(tag_names)

    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        abort(500)

    return render_template('content/form.html', form=form, title='Edit Content', content=content)


@content_bp.route('/delete/<string:content_id>', methods=['POST'])
@login_required
def delete(content_id):
    """Delete content."""
    try:
        client = get_supabase_admin_client()

        # Get content to check permissions
        result = client.table('content').select('author_id, title').eq('id', content_id).single().execute()
        if not result.data:
            abort(404)

        content = result.data

        # Check permissions
        if not current_user.is_admin() and str(content['author_id']) != str(current_user.id):
            flash('You do not have permission to delete this content.', 'danger')
            return redirect(url_for('content.view', content_id=content_id))

        # Delete content (cascade will handle related records)
        client.table('content').delete().eq('id', content_id).execute()

        flash(f'Content "{content["title"]}" has been deleted.', 'success')
        return redirect(url_for('content.list'))

    except Exception as e:
        flash(f'Error deleting content: {str(e)}', 'danger')
        return redirect(url_for('content.view', content_id=content_id))