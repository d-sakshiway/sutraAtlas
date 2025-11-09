from flask import Flask, request, jsonify, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    from config import Config

    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

        # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'pages.login_page'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # register blueprints (import here to avoid circular imports)
    from app.auth.routes import auth_bp
    from app.collections.routes import collections_bp
    from app.suggestions.routes import sugg_bp
    from app.pages.routes import pages_bp
    from app.resources.routes import resources_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(collections_bp)
    app.register_blueprint(sugg_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(resources_bp)

    # create tables for dev convenience
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            pass

    # set user loader
    from app.models import User


    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None

    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import request, redirect, url_for, flash
        # Check if it's an API request
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Authentication required'}), 401
        
        # For web pages, flash a message and redirect to login
        if 'profile' in request.path:
            flash('Please log in to access your profile.', 'info')
        elif 'collections' in request.path:
            flash('Please log in to access your collections.', 'info')
        elif 'resources' in request.path:
            flash('Please log in to manage resources.', 'info')
        elif 'faq' in request.path:
            flash('Please log in to access the FAQ and help features.', 'info')
        else:
            flash('Please log in to access this page.', 'info')
        
        return redirect(url_for('pages.login_page'))

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': str(error.description) if error.description else 'Bad request'}), 400
        return render_template('errors/400.html', error=error), 400

    @app.errorhandler(403)
    def forbidden(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Access forbidden'}), 403
        return render_template('errors/403.html', error=error), 403

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': str(error.description) if error.description else 'Resource not found'}), 404
        return render_template('errors/404.html', error=error), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('errors/500.html', error=error), 500



    # optional admin seeding
    try:
        from app.models import create_admin_if_missing

        create_admin_if_missing(app)
    except Exception:
        pass

    return app
