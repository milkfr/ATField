from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.asset import Host, Zone
from app.libs.success_types import Success


host = Redprint('host')


@host.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', None, type=str)
    ip = request.args.get('ip', '', type=str)
    origin = request.args.get('origin', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    status = request.args.get('status', 1, type=int)
    pagination = Host.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, ip=ip,
                                                    zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                    origin=origin, cpe=cpe, status=status)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': h.uid,
            'ip': h.ip,
            'zone_uid': h.zone_uid,
            'origin': h.origin,
            'cpe': h.cpe,
            'service_count': h.service_count,
            'status': h.status,
            'info': h.info,
        } for h in pagination.items],
        'zones': Zone.recursion_items()
    }
    return Success(msg=data)


@host.route('/service', methods=['GET'])
@auth.login_required
def get_service():
    uid = request.args.get('uid', '', type=str)
    h = Host.get_item_by_uid(uid=uid)
    data = {
        'pageSize': len(h.services),
        'pageNo': 1,
        'totalCount': len(h.services),
        'data': h.services
    }
    return Success(msg=data)


@host.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    origin = data.get('origin')
    zone_uid = data.get('zone_uid')
    with db.auto_commit():
        h = Host.get_item_by_uid(uid=uid)
        h.update(origin=origin, zone_uid=zone_uid)
    return Success()


@host.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    ip = data.get('ip')
    origin = data.get('origin')
    zone_uid = data.get('zone_uid')
    with db.auto_commit():
        Host.save(ip=ip, origin=origin, zone_uid=zone_uid)
    return Success()


@host.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = Host.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        h.activate()
    return Success()


@host.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = Host.get_item_by_uid(uid)
    with db.auto_commit():
        h.remove()
    return Success()
