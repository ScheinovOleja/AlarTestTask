import os

from flask import Flask
from flask_login import LoginManager

from login_app.database import db
from login_app.first.models import MyUsers

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.needs_refresh_message = (u"Session timedout, please re-login")
    login_manager.needs_refresh_message_category = "info"

    from .first.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .first.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
