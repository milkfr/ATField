from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_elasticsearch import FlaskElasticsearch
from config import config


db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()
es = FlaskElasticsearch()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    es.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .probe import probe as probe_blueprint
    app.register_blueprint(probe_blueprint, url_prefix="/probe")

    return app
