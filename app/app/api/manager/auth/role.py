from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.auth import Role, Permission
from app.libs.success_types import Success


role = Redprint('role')


@role.route('', methods=['GET'])
@auth.login_required
def get_list():
    uid = request.args.get('uid', '', type=str)
    name = request.args.get('name', '', type=str)
    status = request.args.get('status', 1, type=int)
    roles = Role.list_items_by_search(uid=uid, name=name, status=status)
    data = {
        'pageSize': len(roles),
        'pageNo': 1,
        'totalCount': len(roles),
        'data': [{
            'uid': r.uid,
            'name': r.name,
            'status': r.status,
            'permissions': [permission.uid for permission in r.permissions]
        } for r in roles],
        'permissions': [{
            'uid': p.uid,
            'endpoint': p.endpoint
        } for p in Permission.list_items()]
    }
    return Success(msg=data)


@role.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    name = data.get('name')
    permissions = data.get('permissions')
    r = Role.get_item_by_uid(uid=uid)
    with db.auto_commit():
        r.update(name=name, permissions=Permission.list_items_by_uids(permissions))
    return Success()


@role.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    name = data.get('name')
    permissions = data.get('permissions')
    with db.auto_commit():
        Role.save(name=name, permissions=Permission.list_items_by_uids(permissions))
    return Success()


@role.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    r = Role.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        r.activate()
    return Success()


@role.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    r = Role.get_item_by_uid(uid)
    with db.auto_commit():
        r.remove()
    return Success()
