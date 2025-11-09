from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Collection, Resource

collections_bp = Blueprint('collections', __name__, url_prefix='/api/collections')


@collections_bp.route('', methods=['GET'])
@login_required
def list_collections():
    query = Collection.query.filter_by(user_id=current_user.id)
    
    # Search query
    q = request.args.get('q', '')
    if q:
        query = query.filter(
            (Collection.name.ilike(f'%{q}%')) | 
            (Collection.description.ilike(f'%{q}%'))
        )
    
    # Sort options
    sort_by = request.args.get('sort', 'created_at')
    if sort_by == 'name':
        query = query.order_by(Collection.name)
    else:  # default: created_at
        query = query.order_by(Collection.created_at.desc())
    
    cols = query.all()
    return jsonify({'collections': [c.to_dict() for c in cols]}), 200


@collections_bp.route('', methods=['POST'])
@login_required
def create_collection():
    data = request.get_json() or {}
    name = data.get('name')
    description = data.get('description')
    if not name:
        return jsonify({'error': 'name required'}), 400
    col = Collection(name=name, description=description, user_id=current_user.id)
    db.session.add(col)
    db.session.commit()
    return jsonify({'collection': col.to_dict()}), 201


@collections_bp.route('/<int:cid>', methods=['GET'])
@login_required
def get_collection(cid):
    col = Collection.query.get_or_404(cid)
    if col.user_id != current_user.id:
        return jsonify({'error': 'forbidden'}), 403
    return jsonify({'collection': col.to_dict()}), 200


@collections_bp.route('/<int:cid>', methods=['PUT'])
@login_required
def update_collection(cid):
    col = Collection.query.get_or_404(cid)
    if col.user_id != current_user.id:
        return jsonify({'error': 'forbidden'}), 403
    data = request.get_json() or {}
    if 'name' in data:
        col.name = data.get('name')
    if 'description' in data:
        col.description = data.get('description')
    db.session.commit()
    return jsonify({'collection': col.to_dict()}), 200


@collections_bp.route('/<int:cid>', methods=['DELETE'])
@login_required
def delete_collection(cid):
    col = Collection.query.get_or_404(cid)
    if col.user_id != current_user.id:
        return jsonify({'error': 'forbidden'}), 403
    db.session.delete(col)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200


# Nested resources
@collections_bp.route('/<int:cid>/resources', methods=['GET'])
@login_required
def list_resources(cid):
    col = Collection.query.get_or_404(cid)
    if col.user_id != current_user.id:
        return jsonify({'error': 'forbidden'}), 403
    
    # Build query with filters
    query = Resource.query.filter_by(collection_id=cid)
    
    # Search query
    q = request.args.get('q', '')
    if q:
        query = query.filter(
            (Resource.title.ilike(f'%{q}%')) | 
            (Resource.authors.ilike(f'%{q}%'))
        )
    
    # Status filter
    status = request.args.get('status', '')
    if status:
        from app.models import StatusEnum
        try:
            status_enum = StatusEnum(status)
            query = query.filter(Resource.status == status_enum)
        except ValueError:
            pass
    
    # Author filter
    author = request.args.get('author', '')
    if author:
        query = query.filter(Resource.authors.ilike(f'%{author}%'))
    
    # Sort options
    sort_by = request.args.get('sort', 'created_at')
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
def create_resource(cid):
    col = Collection.query.get_or_404(cid)
    if col.user_id != current_user.id:
        return jsonify({'error': 'forbidden'}), 403
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return jsonify({'error': 'title required'}), 400
    authors = data.get('authors')
    url = data.get('url')
    status = data.get('status')
    # validate status
    from app.models import StatusEnum

    try:
        status_val = StatusEnum(status) if status else StatusEnum.NOT_STARTED
    except Exception:
        return jsonify({'error': 'invalid status'}), 400

    res = Resource(title=title, authors=authors, url=url, status=status_val, collection_id=cid)
    db.session.add(res)
    db.session.commit()
    return jsonify({'resource': res.to_dict()}), 201
