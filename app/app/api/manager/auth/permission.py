from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.auth import Permission
from app.libs.success_types import Success


permission = Redprint('permission')


@permission.route('', methods=['GET'])
@auth.login_required
def get_list():
    uid = request.args.get('uid', '', type=str)
    endpoint = request.args.get('endpoint', '', type=str)
    status = request.args.get('status', 1, type=int)
    permissions = Permission.list_items_by_search(uid=uid, endpoint=endpoint, status=status)
    data = {
        'pageSize': len(permissions),
        'pageNo': 1,
        'totalCount': len(permissions),
        'data': [{'uid': p.uid, 'endpoint': p.endpoint, 'status': p.status} for p in permissions]
    }
    return Success(msg=data)


@permission.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    p = Permission.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        p.activate()
    return Success()


@permission.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    p = Permission.get_item_by_uid(uid)
    with db.auto_commit():
        p.remove()
    return Success()
