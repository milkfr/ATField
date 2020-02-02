from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models.asset import Service, Zone
from app.libs.success_types import Success


service = Redprint('service')


@service.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    zone_uid = request.args.get('zone_uid', '', type=str)
    uid = request.args.get('uid', '', type=str)
    host_ip = request.args.get('host_ip', '', type=str)
    port = request.args.get('port', '', type=str)
    name = request.args.get('name', '', type=str)
    protocol = request.args.get('protocol', '', type=str)
    tunnel = request.args.get('tunnel', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    status = request.args.get('status', 1, type=int)
    pagination = Service.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid,
                                                       host_ip=host_ip, port=port, status=status, cpe=cpe, name=name,
                                                       zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                       protocol=protocol, tunnel=tunnel)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': s.uid,
            'zone_uid': s.zone_uid,
            'host_uid': s.host_uid,
            'host_ip': s.host_ip,
            'port': s.port,
            'protocol': s.protocol,
            'tunnel': s.tunnel,
            'name': s.name,
            'cpe': s.cpe,
            'status': s.status,
            'info': s.info
        } for s in pagination.items],
        'zones': Zone.recursion_items()
    }
    return Success(msg=data)
