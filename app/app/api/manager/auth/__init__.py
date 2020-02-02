from flask import Blueprint


from app.api.manager.auth.login import login
from app.api.manager.auth.permission import permission
from app.api.manager.auth.role import role
from app.api.manager.auth.user import user


def create_blueprint_auth():
    bp_auth = Blueprint('manager_auth', __name__)
    login.register(bp_auth)
    permission.register(bp_auth)
    role.register(bp_auth)
    user.register(bp_auth)
    return bp_auth
