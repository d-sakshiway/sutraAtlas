from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400

    # Password validation
    if len(password) < 8:
        return jsonify({'error': 'password must be at least 8 characters long'}), 400
    
    if not any(c.isupper() for c in password):
        return jsonify({'error': 'password must contain at least one uppercase letter'}), 400
    
    if not any(c.islower() for c in password):
        return jsonify({'error': 'password must contain at least one lowercase letter'}), 400
    
    if not any(c.isdigit() for c in password):
        return jsonify({'error': 'password must contain at least one number'}), 400

    # Email validation (basic format check)
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return jsonify({'error': 'invalid email format'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'email already registered'}), 409

    user = User(email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'user created', 'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    identifier = data.get('email')
    password = data.get('password')
    if not identifier or not password:
        return jsonify({'error': 'email/username and password required'}), 400

    # allow login by email or username
    try:
        from sqlalchemy import or_

        user = User.query.filter(
            or_(User.email == identifier, User.username == identifier),
            User.is_deleted == False,
        ).first()
    except Exception:
        # fallback to simple email match if sqlalchemy import fails
        user = User.query.filter_by(email=identifier, is_deleted=False).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'invalid credentials'}), 401

    login_user(user)
    return jsonify({'message': 'logged in', 'user': user.to_dict()}), 200


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
def update_me():
    data = request.get_json() or {}
    user = current_user
    if 'username' in data:
        user.username = data.get('username')
    # email change is not allowed currently; could be added with verification
    db.session.commit()
    return jsonify(user.to_dict()), 200


@auth_bp.route('/change-password', methods=['PUT'])
@login_required
def change_password():
    data = request.get_json() or {}
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'error': 'current and new passwords required'}), 400
    
    user = current_user
    if not user.check_password(current_password):
        return jsonify({'error': 'current password is incorrect'}), 401
    
    # Password validation for new password
    if len(new_password) < 8:
        return jsonify({'error': 'new password must be at least 8 characters long'}), 400
    
    if not any(c.isupper() for c in new_password):
        return jsonify({'error': 'new password must contain at least one uppercase letter'}), 400
    
    if not any(c.islower() for c in new_password):
        return jsonify({'error': 'new password must contain at least one lowercase letter'}), 400
    
    if not any(c.isdigit() for c in new_password):
        return jsonify({'error': 'new password must contain at least one number'}), 400
    
    user.set_password(new_password)
    db.session.commit()
    return jsonify({'message': 'password updated successfully'}), 200
