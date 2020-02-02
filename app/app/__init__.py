from app.models import db
from app._flask import Flask
from flask_cors import CORS
from celery import Celery
from config import config


celery = Celery()


def register_blueprints(flask_app):
    from app.api.manager import create_blueprint_manager
    from app.api.restful.v1 import create_blueprint_restful_v1
    for blueprint in create_blueprint_manager():
        flask_app.register_blueprint(blueprint, url_prefix='/api')
    flask_app.register_blueprint(create_blueprint_restful_v1(), url_prefix='/api/v1')


def register_plugins(flask_app):
    CORS(flask_app, resources={r"*": {"origins": "*"}})
    db.init_app(flask_app)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    celery.conf.update(app.config)

    register_plugins(app)
    register_blueprints(app)

    return app
