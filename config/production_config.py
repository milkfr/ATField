# -*- coding: utf-8 -*-

import os

from config.base_config import Config, basedir


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "data.sqlite")