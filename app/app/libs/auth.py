from flask_httpauth import HTTPBasicAuth
from flask import g, request
from app.models.auth.user import User
from app.models.auth.permission import Permission


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, password):
    if password:
        g.current_user = User.get_item_by_name(name=token)
        if g.current_user and g.current_user.verify_password(password):
            permission = Permission.get_item_by_endpoint(request.endpoint)
            if permission:
                return g.current_user.can(permission)
    g.current_user = User.verify_api_auth_token(token)
    if g.current_user:
        permission = Permission.get_item_by_endpoint(request.endpoint)
        if permission:
            return g.current_user.can(permission)
    return False
