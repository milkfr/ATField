from app.libs.redprint import Redprint
from app.libs.auth import auth
from flask import jsonify, current_app, g


token = Redprint('token')


@token.route('', methods=['GET'])
@auth.login_required
def get_token():
    return jsonify({
        'token': g.current_user.generate_api_auth_token(current_app.config['TOKEN_EXPIRATION'])
    })
    pass
