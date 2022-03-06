import os
import random
import string

from flask import Flask
from flask_login import LoginManager

from login_app.models import MyUsers, db

login_manager = LoginManager()


def create_app():
    """
    Создание приложения Flask.
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_letters) for i in range(50))
    # Привязка бд к приложению
    db.init_app(app)
    # Создание всех таблиц
    db.create_all()

    # указание страницы "логина" и привязка к приложению менеджера, для "обработки" входа
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # регистрация блупринтов
    from login_app.server_handler.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from login_app.server_handler.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
