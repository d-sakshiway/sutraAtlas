from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.utils import validate_json_input, get_validated_json

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
@validate_json_input(required_fields=['email', 'password'], optional_fields=['username'])
def register():
    data = get_validated_json()
    email = data['email'].strip().lower()
    password = data['password']
    username = data.get('username', '').strip()

    # Email validation
    if len(email) > 254:  # RFC compliant max length
        return jsonify({'error': 'Email too long'}), 400
    
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return jsonify({'error': 'Invalid email format'}), 400

    # Username validation
    if username:
        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters long'}), 400
        if len(username) > 50:
            return jsonify({'error': 'Username too long (max 50 characters)'}), 400
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return jsonify({'error': 'Username can only contain letters, numbers, hyphens, and underscores'}), 400

    # Password validation
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long'}), 400
    
    if len(password) > 128:
        return jsonify({'error': 'Password too long (max 128 characters)'}), 400
    
    if not any(c.isupper() for c in password):
        return jsonify({'error': 'Password must contain at least one uppercase letter'}), 400
    
    if not any(c.islower() for c in password):
        return jsonify({'error': 'Password must contain at least one lowercase letter'}), 400
    
    if not any(c.isdigit() for c in password):
        return jsonify({'error': 'Password must contain at least one number'}), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Check if username already exists (if provided)
    if username and User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 409

    user = User(email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
@validate_json_input(required_fields=['email', 'password'])
def login():
    data = get_validated_json()
    identifier = data['email'].strip()
    password = data['password']

    # Input validation
    if len(identifier) > 254:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if len(password) > 128:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Allow login by email or username
    try:
        from sqlalchemy import or_

        user = User.query.filter(
            or_(User.email == identifier.lower(), User.username == identifier),
            User.is_deleted == False,
        ).first()
    except Exception:
        # Fallback to simple email match if sqlalchemy import fails
        user = User.query.filter_by(email=identifier.lower(), is_deleted=False).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    login_user(user)
    return jsonify({'message': 'Logged in successfully', 'user': user.to_dict()}), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'logged out'}), 200


# Current user endpoints used by frontend
@auth_bp.route('/me', methods=['GET'])
@login_required
def get_me():
    user = current_user
    return jsonify(user.to_dict()), 200


@auth_bp.route('/me', methods=['PUT'])
@login_required
@validate_json_input(optional_fields=['username'])
def update_me():
    data = get_validated_json()
    user = current_user
    
    if 'username' in data:
        username = data['username'].strip()
        
        # Username validation
        if username:
            if len(username) < 3:
                return jsonify({'error': 'Username must be at least 3 characters long'}), 400
            if len(username) > 50:
                return jsonify({'error': 'Username too long (max 50 characters)'}), 400
            
            import re
            if not re.match(r'^[a-zA-Z0-9_-]+$', username):
                return jsonify({'error': 'Username can only contain letters, numbers, hyphens, and underscores'}), 400
            
            # Check if username is already taken by another user
            existing_user = User.query.filter_by(username=username).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'Username already taken'}), 409
        
        user.username = username
    
    db.session.commit()
    return jsonify(user.to_dict()), 200


@auth_bp.route('/change-password', methods=['PUT'])
@login_required
@validate_json_input(required_fields=['current_password', 'new_password'])
def change_password():
    data = get_validated_json()
    current_password = data['current_password']
    new_password = data['new_password']
    
    # Input length validation
    if len(current_password) > 128 or len(new_password) > 128:
        return jsonify({'error': 'Password too long'}), 400
    
    user = current_user
    if not user.check_password(current_password):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    # Check if new password is same as current
    if current_password == new_password:
        return jsonify({'error': 'New password must be different from current password'}), 400
    
    # Password validation for new password
    if len(new_password) < 8:
        return jsonify({'error': 'New password must be at least 8 characters long'}), 400
    
    if not any(c.isupper() for c in new_password):
        return jsonify({'error': 'New password must contain at least one uppercase letter'}), 400
    
    if not any(c.islower() for c in new_password):
        return jsonify({'error': 'New password must contain at least one lowercase letter'}), 400
    
    if not any(c.isdigit() for c in new_password):
        return jsonify({'error': 'New password must contain at least one number'}), 400
    
    user.set_password(new_password)
    db.session.commit()
    return jsonify({'message': 'Password updated successfully'}), 200
