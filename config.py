import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BASEDIR = basedir
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "hard to guess string")
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_DEVELOPMENT_DATABASE_URI",
                                             "sqlite:///"+os.path.join(basedir, "data-dev.sqlite"))
    ELASTICSEARCH_HOST = os.environ.get("FLASK_ELASTICSEARCH_HOST", "localhost:9200")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_PRODUCTION_DATABASE_URI",
                                             "sqlite:///"+os.path.join(basedir, "data-pro.sqlite"))


config = {
    "default": DevelopmentConfig,
    "production": ProductionConfig,
    "development": DevelopmentConfig,
}
