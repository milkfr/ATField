import os

basedir = os.path.abspath('.')


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SLQALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):  # 这个方法的用法不是很懂
        pass