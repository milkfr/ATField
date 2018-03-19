import os
from config.base_config import Config, basedir

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
                                     'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')