from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from models import db
from web.web import web_page
from api.api import api_bp


def create_app():
    app = Flask('app')
    app.config.from_object('settings')
    app.register_blueprint(web_page)
    app.register_blueprint(api_bp)
    db.init_app(app=app)
    Migrate(app=app, db=db)
    CORS(app=app)

    return app
