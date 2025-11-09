"""
Utility functions for validation and error handling
"""
from functools import wraps
from flask import jsonify, abort, request
from flask_login import current_user
from app.models import Collection, Resource


def validate_id(id_value, name="ID"):
    """Validate that an ID is a positive integer"""
    try:
        id_int = int(id_value)
        if id_int <= 0:
            raise ValueError("ID must be positive")
        return id_int
    except (ValueError, TypeError):
        abort(400, description=f"Invalid {name}: must be a positive integer")


def validate_ownership(model_class, model_id, user_id=None):
    """Validate that current user owns the resource"""
    if user_id is None:
        user_id = current_user.id
    
    if model_class == Collection:
        item = Collection.query.filter_by(id=model_id, user_id=user_id).first()
    elif model_class == Resource:
        # For resources, check ownership through collection
        resource = Resource.query.get(model_id)
        if not resource:
            return None
        collection = Collection.query.filter_by(id=resource.collection_id, user_id=user_id).first()
        item = resource if collection else None
    else:
        item = None
    
    if not item:
        abort(404, description="Resource not found or access denied")
    
    return item


def validate_json_input(required_fields=None, optional_fields=None):
    """Decorator to validate JSON input"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({'error': 'JSON input required'}), 400
            
            # Check required fields
            if required_fields:
                missing_fields = [field for field in required_fields if not data.get(field)]
                if missing_fields:
                    return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
            
            # Filter only allowed fields
            allowed_fields = (required_fields or []) + (optional_fields or [])
            if allowed_fields:
                filtered_data = {k: v for k, v in data.items() if k in allowed_fields}
                request._validated_json = filtered_data
            else:
                request._validated_json = data
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_validated_json():
    """Get the validated JSON data from request"""
    return getattr(request, '_validated_json', {})


def safe_query_param(param_name, default='', max_length=100):
    """Safely get and validate query parameters"""
    value = request.args.get(param_name, default)
    if len(value) > max_length:
        value = value[:max_length]
    # Basic XSS prevention
    value = value.replace('<', '').replace('>', '').replace('"', '').replace("'", '')
    return value.strip()


def validate_enum_value(value, enum_class, field_name):
    """Validate enum values"""
    if not value:
        return None
    
    try:
        return enum_class(value)
    except ValueError:
        valid_values = [e.value for e in enum_class]
        abort(400, description=f"Invalid {field_name}. Valid values: {', '.join(valid_values)}")