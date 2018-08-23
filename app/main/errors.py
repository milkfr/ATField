from flask import request

from . import main


# 经过测试，main中定义了app_errorhandler方法，abort以后会调用定义的方法，其他蓝本如果也定义的app_errorhandler，则会调用它们自己的

@main.app_errorhandler(403)
def forbidden(e):
    return "403"


@main.app_errorhandler(404)
def page_not_found(e):
    return "404"


@main.app_errorhandler(500)
def internal_server_error(e):
    return "500"
