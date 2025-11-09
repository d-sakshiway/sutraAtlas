import os
from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db


class StatusEnum(Enum):
    NOT_STARTED = 'Not Started'
    IN_PROGRESS = 'In Progress'
    PAUSED = 'Paused'
    COMPLETED = 'Completed'


def utcnow():
    return datetime.utcnow()


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(150), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), nullable=False, default='user')
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    collections = db.relationship('Collection', backref='owner', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role == 'admin'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'is_deleted': self.is_deleted,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<User {self.email}>'


class Collection(db.Model):
    __tablename__ = 'collection'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    resources = db.relationship('Resource', backref='collection', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<Collection {self.name}>'


class Resource(db.Model):
    __tablename__ = 'resource'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False, index=True)
    authors = db.Column(db.String(500), nullable=True)
    url = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.NOT_STARTED)
    last_read_date = db.Column(db.DateTime, nullable=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    def authors_list(self):
        if not self.authors:
            return []
        return [a.strip() for a in self.authors.split(',') if a.strip()]

    # allow setting status via string helper
    def set_status(self, status_str):
        from app.models import StatusEnum

        try:
            self.status = StatusEnum(status_str)
        except Exception:
            pass

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'authors_list': self.authors_list(),
            'url': self.url,
            'status': self.status.value if self.status else None,
            'last_read_date': self.last_read_date.isoformat() if self.last_read_date else None,
            'collection_id': self.collection_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<Resource {self.title}>'


def create_admin_if_missing(app):
    """Create a default admin user if environment variables ADMIN_EMAIL and ADMIN_PASSWORD are set and no admin exists.

    This function is safe to call from the app factory; it will only create a user when there are no users yet or no admin.
    """
    from sqlalchemy.exc import SQLAlchemyError

    admin_email = os.environ.get('ADMIN_EMAIL')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')

    if not admin_email or not admin_password:
        return

    with app.app_context():
        try:
            existing_admin = User.query.filter_by(email=admin_email).first()
            if existing_admin:
                if existing_admin.role != 'admin':
                    existing_admin.role = 'admin'
                    db.session.commit()
                return

            # Only create admin if there are no users at all or admin does not exist
            any_users = User.query.first()
            if any_users:
                # Do not auto-create admin if users already exist (security)
                return

            admin = User(email=admin_email, username=admin_username, role='admin')
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return
