from flask import Flask
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

    # optional admin seeding
    try:
        from app.models import create_admin_if_missing

        create_admin_if_missing(app)
    except Exception:
        pass

    return app
