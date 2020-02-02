from flask import request
from app.libs.redprint import Redprint
from app.libs.auth import auth
from app.libs.success_types import Success, NotContent
from app.models.asset import Domain, Host, Service, Zone, HTTP, CGI
from app.models import db


asset = Redprint('asset')


@asset.route('/domain', methods=['GET'])
@auth.login_required
def get_domain():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    name = request.args.get('name', '', type=str)
    domain_type = request.args.get('type', '', type=str)
    origin = request.args.get('origin', '', type=str)
    pagination = Domain.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid,
                                                      zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                      name=name, type=domain_type, origin=origin, status=1)
    return Success(msg=pagination)


@asset.route('/host', methods=['GET'])
@auth.login_required
def get_host():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    ip = request.args.get('ip', '', type=str)
    origin = request.args.get('origin', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    pagination = Host.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, ip=ip,
                                                    zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                    origin=origin, cpe=cpe, status=1)
    return Success(msg=pagination)


@asset.route('/service', methods=['GET'])
@auth.login_required
def get_service():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    host_ip = request.args.get('host_ip', '', type=str)
    port = request.args.get('port', '', type=str)
    name = request.args.get('name', '', type=str)
    protocol = request.args.get('protocol', '', type=str)
    tunnel = request.args.get('tunnel', '', type=str)
    cpe = request.args.get('cpe', '', type=str)
    pagination = Service.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, host_ip=host_ip,
                                                       port=port, status=1, cpe=cpe, name=name,
                                                       zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                       protocol=protocol, tunnel=tunnel)
    return Success(msg=pagination)


@asset.route('/http', methods=['GET'])
@auth.login_required
def get_http():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', '', type=str)
    website = request.args.get('website', '', type=str)
    business = request.args.get('business', '', type=str)
    title = request.args.get('title', '', type=str)
    status = request.args.get('status', 1, type=int)
    pagination = HTTP.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, website=website,
                                                    zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                    business=business, title=title, status=status)
    return Success(msg=pagination)


@asset.route('/cgi', methods=['GET'])
@auth.login_required
def get_cgi():
    page_no = request.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    http_uid = request.args.get('http_uid', '', type=str)
    url = request.args.get('url', '', type=str)
    method = request.args.get('method', '', type=str)
    code = request.args.get('code', 200, type=int)
    pagination = CGI.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid,
                                                   http_uid=http_uid, url=url, method=method, code=code)
    return Success(msg=pagination)


@asset.route('/domain/batch', methods=['POST'])
@auth.login_required
def domain_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                domain = Domain.query.filter(Domain.name == info.get('name')).first()
                if domain and domain.status == 0:
                    domain.activate()
                    domain.update(**info)
                else:
                    Domain.save(**info)
    elif action == 'delete':
        with db.auto_commit():
            for name in info_list:
                domain = Domain.get_item_by_name(name)
                domain.remove()
    return NotContent()


@asset.route('/host/batch', methods=['POST'])
@auth.login_required
def host_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                host = Host.query.filter(Host.ip == info.get('ip')).first()
                if host and host.status == 0:
                    host.activate()
                    host.update(**info)
                else:
                    Host.save(**info)
    elif action == 'delete':
        with db.auto_commit():
            for ip in info_list:
                host = Host.get_item_by_ip(ip)
                host.remove()
    return NotContent()


@asset.route('/http/batch', methods=['POST'])
@auth.login_required
def http_batch():
    data = request.get_json(silent=True)
    action = data.get('action')
    info_list = data.get('info')
    if action == 'add':
        with db.auto_commit():
            for info in info_list:
                http = HTTP.query.filter(HTTP.website == info.get('website')).first()
                if http and http.status == 0:
                    http.activate()
                    http.update(**info)
                else:
                    HTTP.save(**info)
    elif action == 'delete':
        with db.auto_commit():
            for website in info_list:
                http = HTTP.get_item_by_website(website)
                http.remove()
    return NotContent()
