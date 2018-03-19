from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

from config import config

db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()


def create_app(config_name):
    """
    工厂函数
    单个文件中开发程序，程序在全局作用域中创建，无法动态修改配置
    运行脚本时，程序实例已经创建，再修改配置为时已晚
    解决方法时延迟创建程序实例，把创建过程移到可显式调用的工厂函数中
    这种方法不仅可以给脚本留出配置程序的时间，还能够创建多个程序实例
    在测试中非常有用
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # from_object是什么方法，这一句没有弄明白

    db.init_app(app)  # 涉及到flask插件的用法，没有弄明白
    bootstrap.init_app(app)
    csrf.init_app(app)

    # 附加路由和自定义错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app
