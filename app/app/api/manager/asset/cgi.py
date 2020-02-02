from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.asset import CGI, HTTP
from app.libs.success_types import Success
import json


cgi = Redprint('cgi')


@cgi.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    http_uid = request.args.get('http_uid', '', type=str)
    url = request.args.get('url', '', type=str)
    method = request.args.get('method', '', type=str)
    code = request.args.get('code', 200, type=int)
    status = request.args.get('status', 1, type=int)
    pagination = CGI.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, status=status,
                                                   http_uid=http_uid, url=url, method=method, code=code)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': c.uid,
            'http_uid': c.http_uid,
            'url': c.url,
            'method': c.method,
            'code': c.code,
            'status': c.status,
            'info': c.info
        } for c in pagination.items]
    }
    return Success(msg=data)


@cgi.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    http_uid = data.get('http_uid')
    url = data.get('url')
    method = data.get('method')
    code = data.get('code')
    info = json.loads(data.get('info'))
    c = CGI.get_item_by_uid(uid=uid)
    with db.auto_commit():
        c.update(http_uid=http_uid, url=url, method=method, code=code, info=info)
    return Success()


@cgi.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    http_uid = data.get('http_uid')
    url = data.get('url')
    method = data.get('method')
    code = data.get('code')
    info = json.loads(data.get('info'))
    with db.auto_commit():
        CGI.save(http_uid=http_uid, url=url, method=method, code=code, info=info)
    return Success()


@cgi.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    c = CGI.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        c.activate()
    return Success()


@cgi.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    c = CGI.get_item_by_uid(uid)
    with db.auto_commit():
        c.remove()
    return Success()
