from app.libs.redprint import Redprint
from flask import request, g, current_app
from app.libs.auth import auth
from app.models.auth import User, Role, Permission
from app.libs.error_types import AuthFailedException
from app.libs.success_types import Success


login = Redprint('login')


@login.route('/token', methods=['POST'])
def get_token():
    data = request.get_json(silent=True)
    username = data.get('username')
    password = data.get('password')
    user = User.get_item_by_name(name=username)
    if not user or not user.verify_password(password):
        return AuthFailedException(msg='user or secret error')
    return Success(msg={
        'token': user.generate_api_auth_token(current_app.config['TOKEN_EXPIRATION'])
    })


@login.route('/user_info', methods=['GET'])
@auth.login_required
def get_user_info():
    data = {
        'uid': g.current_user.uid,
        'name': g.current_user.name,
        'roles': [],
        'permissions': []
    }
    permission_list = {}
    for role in g.current_user.roles:
        for permission in role.permissions:
            module, action = permission.endpoint.split('+')
            if not permission_list.get(module, None):
                permission_list[module] = []
            permission_list[module].append(action)
        data['roles'].append(
            {
                'uid': role.uid,
                'name': role.name,
            }
        )
    for module, action in permission_list.items():
        data['permissions'].append({
            'name': module,
            'actions': action
        })
    return Success(msg=data)
