from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Resource, Collection, StatusEnum
from app.utils import validate_id, validate_ownership, validate_json_input, get_validated_json, validate_enum_value

resources_bp = Blueprint('resources', __name__, url_prefix='/api/resources')





@resources_bp.route('/<int:rid>', methods=['GET'])
@login_required
def get_resource(rid):
    rid = validate_id(rid, "Resource ID")
    res = validate_ownership(Resource, rid)
    return jsonify({'resource': res.to_dict()}), 200


@resources_bp.route('/<int:rid>', methods=['PUT'])
@login_required
@validate_json_input(optional_fields=['title', 'authors', 'url', 'status'])
def update_resource(rid):
    rid = validate_id(rid, "Resource ID")
    res = validate_ownership(Resource, rid)
    data = get_validated_json()
    
    if 'title' in data:
        title = data['title'].strip()
        if not title:
            return jsonify({'error': 'Title cannot be empty'}), 400
        if len(title) > 300:
            return jsonify({'error': 'Title too long (max 300 characters)'}), 400
        res.title = title
    
    if 'authors' in data:
        authors = data['authors'].strip()
        if len(authors) > 500:
            return jsonify({'error': 'Authors field too long (max 500 characters)'}), 400
        res.authors = authors
    
    if 'url' in data:
        url = data['url'].strip()
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
        res.url = url
    
    if 'status' in data:
        status_val = validate_enum_value(data['status'], StatusEnum, 'status')
        if status_val:
            res.status = status_val
    
    db.session.commit()
    return jsonify({'resource': res.to_dict()}), 200


@resources_bp.route('/<int:rid>', methods=['DELETE'])
@login_required
def delete_resource(rid):
    rid = validate_id(rid, "Resource ID")
    res = validate_ownership(Resource, rid)
    
    db.session.delete(res)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200
