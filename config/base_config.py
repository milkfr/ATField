# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass