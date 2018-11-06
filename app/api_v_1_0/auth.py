from . import api_v_1_0
from app.models.auth import User, Permission
from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify, request


auth = HTTPBasicAuth()


@api_v_1_0.route("/token", methods=["GET"])
def get_token():
    return jsonify({"token": g.current_user.generate_api_auth_token(expiration=3600), 'expiration': 3600})


@auth.verify_password
def verify_password(username_or_auth_token, password):
    if username_or_auth_token == "":
        return False
    if password == "":
        g.current_user = User.verify_api_auth_token(username_or_auth_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter(User.name == username_or_auth_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    response = jsonify({"error": "Notfound"})
    response.status_code = 404
    return response


@api_v_1_0.before_request
@auth.login_required
def before_request():
    # add permission limit
    permission = Permission.query.filter(Permission.endpoint == request.endpoint).first()
    if not g.current_user.can(permission):
        response = jsonify({"error": "Notfound"})
        response.status_code = 404
        return response
