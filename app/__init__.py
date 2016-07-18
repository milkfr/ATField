# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)

    # 附加路由和自定义错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from app.role import role as role_blueprint
    app.register_blueprint(role_blueprint, url_prefix="/role")

    from app.function import function as function_blueprint
    app.register_blueprint(function_blueprint, url_prefix="/function")

    from app.document import document as document_blueprint
    app.register_blueprint(document_blueprint, url_prefix="/document")

    return app
