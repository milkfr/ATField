# -*- coding: utf-8 -*-

from config.development_config import DevelopmentConfig
from config.testing_config import TestingConfig
from config.production_config import ProductionConfig

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
