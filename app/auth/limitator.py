from flask import session, request, redirect, url_for, abort
from . import auth
from ..models.auth import User, Permission


@auth.before_app_request
def permission_required():

    # 白名单通过
    whitelist = ["auth.login", "auth.logout", "main.index", "bootstrap.static", "static"]
    if request.endpoint in whitelist:
        return

    # 没有登录
    user_id = session.get("id", None)
    if not user_id:
        return redirect(url_for('auth.login'))

    # 登录失效
    current_user = User.query.filter(User.id == user_id).first()
    if not current_user:
        return redirect(url_for('auth.login'))

    # 没有权限
    permission = Permission.query.filter(Permission.endpoint == request.endpoint).first()
    if not current_user.can(permission):
        abort(404)
