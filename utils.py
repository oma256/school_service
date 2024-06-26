from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from models import User, db
from web.web import web_page
from api.api import api_bp


def create_app():
    app = Flask('app')
    app.config.from_object('settings')

    login_manager = LoginManager()
    login_manager.login_view = 'web.login'
    login_manager.init_app(app)
    login_manager.login_message = 'Введите почту и пароль'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(web_page)
    app.register_blueprint(api_bp)
    db.init_app(app=app)
    Migrate(app=app, db=db)
    CORS(app=app)
    JWTManager(app=app)

    return app
