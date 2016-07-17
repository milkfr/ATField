# -*- coding: utf-8 -*-

import os

from config.base_config import Config, basedir


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "data-test.sqlite")
