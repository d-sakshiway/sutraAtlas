from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Collection, Resource, StatusEnum
from app.utils import validate_id, validate_ownership, validate_json_input, get_validated_json, safe_query_param, validate_enum_value

collections_bp = Blueprint('collections', __name__, url_prefix='/api/collections')


@collections_bp.route('', methods=['GET'])
@login_required
def list_collections():
    query = Collection.query.filter_by(user_id=current_user.id)
    
    # Search query with safe parameter handling
    q = safe_query_param('q', '', 200)
    if q:
        query = query.filter(
            (Collection.name.ilike(f'%{q}%')) | 
            (Collection.description.ilike(f'%{q}%'))
        )
    
    # Sort options with validation
    sort_by = safe_query_param('sort', 'created_at', 20)
    if sort_by == 'name':
        query = query.order_by(Collection.name)
    else:  # default: created_at
        query = query.order_by(Collection.created_at.desc())
    
    cols = query.all()
    return jsonify({'collections': [c.to_dict() for c in cols]}), 200


@collections_bp.route('', methods=['POST'])
@login_required
@validate_json_input(required_fields=['name'], optional_fields=['description'])
def create_collection():
    data = get_validated_json()
    name = data['name'].strip()
    description = data.get('description', '').strip()
    
    # Validate name length
    if len(name) > 200:
        return jsonify({'error': 'Collection name too long (max 200 characters)'}), 400
    if len(description) > 1000:
        return jsonify({'error': 'Description too long (max 1000 characters)'}), 400
    
    col = Collection(name=name, description=description, user_id=current_user.id)
    db.session.add(col)
    db.session.commit()
    return jsonify({'collection': col.to_dict()}), 201


@collections_bp.route('/<int:cid>', methods=['GET'])
@login_required
def get_collection(cid):
    cid = validate_id(cid, "Collection ID")
    col = validate_ownership(Collection, cid)
    return jsonify({'collection': col.to_dict()}), 200


@collections_bp.route('/<int:cid>', methods=['PUT'])
@login_required
@validate_json_input(optional_fields=['name', 'description'])
def update_collection(cid):
    cid = validate_id(cid, "Collection ID")
    col = validate_ownership(Collection, cid)
    data = get_validated_json()
    
    if 'name' in data:
        name = data['name'].strip()
        if not name:
            return jsonify({'error': 'Collection name cannot be empty'}), 400
        if len(name) > 200:
            return jsonify({'error': 'Collection name too long (max 200 characters)'}), 400
        col.name = name
    
    if 'description' in data:
        description = data['description'].strip()
        if len(description) > 1000:
            return jsonify({'error': 'Description too long (max 1000 characters)'}), 400
        col.description = description
    
    db.session.commit()
    return jsonify({'collection': col.to_dict()}), 200


@collections_bp.route('/<int:cid>', methods=['DELETE'])
@login_required
def delete_collection(cid):
    cid = validate_id(cid, "Collection ID")
    col = validate_ownership(Collection, cid)
    db.session.delete(col)
    db.session.commit()
    return jsonify({'message': 'Collection deleted successfully'}), 200


# Nested resources
@collections_bp.route('/<int:cid>/resources', methods=['GET'])
@login_required
def list_resources(cid):
    cid = validate_id(cid, "Collection ID")
    col = validate_ownership(Collection, cid)
    
    # Build query with filters
    query = Resource.query.filter_by(collection_id=cid)
    
    # Search query with safe parameter handling
    q = safe_query_param('q', '', 200)
    if q:
        query = query.filter(
            (Resource.title.ilike(f'%{q}%')) | 
            (Resource.authors.ilike(f'%{q}%'))
        )
    
    # Status filter with validation
    status = safe_query_param('status', '', 20)
    if status:
        status_enum = validate_enum_value(status, StatusEnum, 'status')
        if status_enum:
            query = query.filter(Resource.status == status_enum)
    
    # Author filter
    author = safe_query_param('author', '', 100)
    if author:
        query = query.filter(Resource.authors.ilike(f'%{author}%'))
    
    # Sort options with validation
    sort_by = safe_query_param('sort', 'created_at', 20)
    if sort_by == 'title':
        query = query.order_by(Resource.title)
    elif sort_by == 'status':
        query = query.order_by(Resource.status)
    else:  # default: created_at
        query = query.order_by(Resource.created_at.desc())
    
    res = query.all()
    return jsonify({'resources': [r.to_dict() for r in res]}), 200


@collections_bp.route('/<int:cid>/resources', methods=['POST'])
@login_required
@validate_json_input(required_fields=['title'], optional_fields=['authors', 'url', 'status'])
def create_resource(cid):
    cid = validate_id(cid, "Collection ID")
    col = validate_ownership(Collection, cid)
    data = get_validated_json()
    
    title = data['title'].strip()
    if len(title) > 300:
        return jsonify({'error': 'Title too long (max 300 characters)'}), 400
    
    authors = data.get('authors', '').strip()
    if len(authors) > 500:
        return jsonify({'error': 'Authors field too long (max 500 characters)'}), 400
    
    url = data.get('url', '').strip()
    if len(url) > 1000:
        return jsonify({'error': 'URL too long (max 1000 characters)'}), 400
    
    # Validate URL format if provided
    if url:
        import re
        url_pattern = r'^https?://.+'
        if not re.match(url_pattern, url, re.IGNORECASE):
            # Try to fix common URL issues
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
    
    # Validate status
    status = data.get('status')
    status_val = validate_enum_value(status, StatusEnum, 'status') or StatusEnum.NOT_STARTED

    res = Resource(title=title, authors=authors, url=url, status=status_val, collection_id=cid)
    db.session.add(res)
    db.session.commit()
    return jsonify({'resource': res.to_dict()}), 201
