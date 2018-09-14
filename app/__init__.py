from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_elasticsearch import FlaskElasticsearch
from flask_mail import Mail
from celery import Celery
from config import config, DevelopmentConfig


db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()
es = FlaskElasticsearch()
mail = Mail()
celery = Celery(__name__,
                backend=DevelopmentConfig.CELERY_RESULT_BACKEND,
                broker=DevelopmentConfig.CELERY_BROKER_URL)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    es.init_app(app)
    mail.init_app(app)
    celery.conf.update(app.config)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .probe import probe as probe_blueprint
    app.register_blueprint(probe_blueprint, url_prefix="/probe")

    return app

