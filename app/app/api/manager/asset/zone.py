from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.asset import Zone
from app.libs.success_types import Success


zone = Redprint('zone')


@zone.route('', methods=['GET'])
@auth.login_required
def get_list():
    zones = Zone.recursion_items()
    data = {
        'pageSize': len(zones),
        'pageNo': 1,
        'totalCount': len(zones),
        'data': zones
    }
    return Success(msg=data)


@zone.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    name = data.get('name')
    z = Zone.get_item_by_uid(uid=uid)
    with db.auto_commit():
        z.update(name=name)
    return Success()


@zone.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    name = data.get('name')
    parent_uid = data.get('parent_uid')
    with db.auto_commit():
        Zone.save(name=name, parent_uid=parent_uid)
    return Success()


@zone.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    z = Zone.get_item_by_uid(uid)
    with db.auto_commit():
        z.remove()
    return Success()
