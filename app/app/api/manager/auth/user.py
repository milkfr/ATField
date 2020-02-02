from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.auth import Permission, User, Role
from app.libs.success_types import Success


user = Redprint('user')


@user.route('', methods=['GET'])
@auth.login_required
def get_list():
    uid = request.args.get('uid', '', type=str)
    name = request.args.get('name', '', type=str)
    status = request.args.get('status', 1, type=int)
    users = User.list_items_by_search(uid=uid, name=name, status=status)
    data = {
        'pageSize': len(users),
        'pageNo': 1,
        'totalCount': len(users),
        'data': [{
            'uid': u.uid,
            'name': u.name,
            'status': u.status,
            'roles': [r.uid for r in u.roles]
        } for u in users],
        'roles': [{
            'uid': r.uid,
            'name': r.name,
            'permissions': [p.uid for p in r.permissions],
        } for r in Role.list_items()],
        'permissions': [{
            'uid': p.uid,
            'endpoint': p.endpoint
        } for p in Permission.list_items()],
    }
    for u in data['data']:
        u['permissions'] = set()
        for r in data['roles']:
            if r['uid'] in u['roles']:
                for permission in r['permissions']:
                    u['permissions'].add(permission)
        u['permissions'] = list(u['permissions'])
    return Success(msg=data)


@user.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    name = data.get('name')
    roles = data.get('roles')
    u = User.get_item_by_uid(uid=uid)
    with db.auto_commit():
        u.update(name=name, roles=Role.list_items_by_uids(roles))
    return Success()


@user.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    name = data.get('name')
    roles = data.get('roles')
    password = data.get('password')
    with db.auto_commit():
        User.save(name=name, roles=Role.list_items_by_uids(roles), password=password)
    return Success()


@user.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    u = User.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        u.activate()
    return Success()


@user.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    u = User.get_item_by_uid(uid)
    with db.auto_commit():
        u.remove()
    return Success()
