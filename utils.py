from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from models import db


def create_app():
    app = Flask('app')
    app.config.from_object('settings')
    db.init_app(app=app)
    Migrate(app=app, db=db)
    CORS(app=app)

    return app
