from flask import session, request, redirect, url_for, abort
from . import auth
from ..models.auth import User, Permission

@auth.before_app_request
def permission_required():
    WHITELIST = ["auth.login", "auth.logout", "main.index"]
    if request.endpoint in WHITELIST:
        return
    id = session.get("id", None)
    if not id:
        return redirect(url_for('auth.login'))
    current_user = User.query.filter(User.id==id).first()
    permission = Permission.query.filter(Permission.endpoint==request.endpoint).first()
    if not current_user.can(permission):
        abort(403)


