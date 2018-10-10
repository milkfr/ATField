from . import api_v_1_0
from app.models.auth import User
from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify


auth = HTTPBasicAuth()


@api_v_1_0.route("/token")
def get_token():
    return jsonify({"token": g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})


@auth.verify_password
def verify_password(username_or_auth_token, password):
    if username_or_auth_token is None:
        return False
    if password is None:
        g.current_user = User.verify_api_auth_token(username_or_auth_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter(User.name == username_or_auth_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@api_v_1_0.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')



