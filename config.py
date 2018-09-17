import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=".flaskenv")
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BASEDIR = basedir
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "hard to guess string")
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get("FLASK_MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("FLASK_MAIL_PASSWORD")
    MAIL_SUBJECT_PREFIX = "[milkfr]"
    MAIL_SENDER = os.environ.get("FLASK_MAIL_USERNAME")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_DATABASE_URI",
                                             "sqlite:///"+os.path.join(basedir, "data-dev.sqlite"))
    ELASTICSEARCH_HOST = os.environ.get("FLASK_ELASTICSEARCH_HOST", "localhost:9200")
    CELERY_RESULT_BACKEND = os.environ.get("FLASK_CELERY_RESULT_BACKEND")
    CELERY_BROKER_URL = os.environ.get("FLASK_CELERY_BROKER_URL")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_DATABASE_URI",
                                             "sqlite:///"+os.path.join(basedir, "data-pro.sqlite"))


config = {
    "default": DevelopmentConfig,
    "production": ProductionConfig,
    "development": DevelopmentConfig,
}
