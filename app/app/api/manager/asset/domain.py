from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.asset import Domain, Zone
from app.libs.success_types import Success
import json


domain = Redprint('domain')


@domain.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    name = request.args.get('name', '', type=str)
    domain_type = request.args.get('type', '', type=str)
    origin = request.args.get('origin', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    status = request.args.get('status', 1, type=int)
    pagination = Domain.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid,
                                                      zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                      name=name, type=domain_type, origin=origin, status=status)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': d.uid,
            'name': d.name,
            'type': d.type,
            'origin': d.origin,
            'zone_uid': d.zone_uid,
            'status': d.status,
            'info': d.info
        } for d in pagination.items],
        'zones': Zone.recursion_items()
    }
    return Success(msg=data)


@domain.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    domain_type = int(data.get('type'))
    origin = data.get('origin')
    info = json.loads(data.get('info'))
    zone_uid = data.get('zone_uid')
    with db.auto_commit():
        d = Domain.get_item_by_uid(uid=uid)
        d.update(type=domain_type, origin=origin, zone_uid=zone_uid, info=info)
    return Success()


@domain.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    name = data.get('name')
    domain_type = int(data.get('type'))
    origin = data.get('origin')
    info = json.loads(data.get('info'))
    zone_uid = data.get('zone_uid')
    with db.auto_commit():
        Domain.save(type=domain_type, origin=origin, name=name, info=info, zone_uid=zone_uid)
    return Success()


@domain.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    d = Domain.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        d.activate()
    return Success()


@domain.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    d = Domain.get_item_by_uid(uid)
    with db.auto_commit():
        d.remove()
    return Success()
