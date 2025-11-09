from flask import Blueprint, request, jsonify, current_app
from .service import query_openlibrary

sugg_bp = Blueprint('suggestions', __name__, url_prefix='/api/suggestions')


@sugg_bp.route('', methods=['GET'])
def suggest():
    q = request.args.get('q', '')
    try:
        limit = int(request.args.get('limit', 8))
    except Exception:
        limit = 8
    base = current_app.config.get('METADATA_API', 'https://openlibrary.org')
    try:
        suggestions = query_openlibrary(q, limit=limit, base_url=base)
        return jsonify({'query': q, 'suggestions': suggestions}), 200
    except Exception as e:
        return jsonify({'error': 'failed to fetch suggestions', 'details': str(e)}), 502
