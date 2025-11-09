from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Resource, Collection

resources_bp = Blueprint('resources', __name__, url_prefix='/api/resources')


def _check_owner(resource):
    # Ensure current_user owns the resource via collection
    col = Collection.query.get(resource.collection_id)
    return col and col.user_id == current_user.id


@resources_bp.route('/<int:rid>', methods=['GET'])
@login_required
def get_resource(rid):
    res = Resource.query.get_or_404(rid)
    if not _check_owner(res):
        return jsonify({'error': 'forbidden'}), 403
    return jsonify({'resource': res.to_dict()}), 200


@resources_bp.route('/<int:rid>', methods=['PUT'])
@login_required
def update_resource(rid):
    res = Resource.query.get_or_404(rid)
    if not _check_owner(res):
        return jsonify({'error': 'forbidden'}), 403
    data = request.get_json() or {}
    if 'title' in data:
        res.title = data.get('title')
    if 'authors' in data:
        res.authors = data.get('authors')
    if 'url' in data:
        res.url = data.get('url')
    if 'status' in data:
        try:
            from app.models import StatusEnum

            res.status = StatusEnum(data.get('status'))
        except Exception:
            return jsonify({'error': 'invalid status'}), 400
    db.session.commit()
    return jsonify({'resource': res.to_dict()}), 200


@resources_bp.route('/<int:rid>', methods=['DELETE'])
@login_required
def delete_resource(rid):
    res = Resource.query.get_or_404(rid)
    if not _check_owner(res):
        return jsonify({'error': 'forbidden'}), 403
    db.session.delete(res)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200
