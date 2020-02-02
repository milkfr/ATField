from app.libs.redprint import Redprint
from flask import request
from app.libs.auth import auth
from app.models import db
from app.models.asset import HTTP, Zone
from app.libs.success_types import Success
import json


http = Redprint('http')


@http.route('', methods=['GET'])
@auth.login_required
def get_list():
    page_no = request.args.get('pageNo', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    uid = request.args.get('uid', '', type=str)
    zone_uid = request.args.get('zone_uid', None, type=str)
    website = request.args.get('website', '', type=str)
    business = request.args.get('business', '', type=str)
    title = request.args.get('title', '', type=str)
    status = request.args.get('status', 1, type=int)
    pagination = HTTP.list_items_paginate_by_search(page=page_no, per_page=page_size, uid=uid, website=website,
                                                    zone_list=Zone.recursion_children_uid_list(zone_uid),
                                                    business=business, title=title, status=status)
    data = {
        'pageSize': pagination.per_page,
        'pageNo': pagination.page,
        'totalCount': pagination.total,
        'data': [{
            'uid': h.uid,
            'website': h.website,
            'zone_uid': h.zone_uid,
            'title': h.title,
            'business': h.business,
            'status': h.status,
            'info': h.info,
        } for h in pagination.items],
        'zones': Zone.recursion_items()
    }
    return Success(msg=data)


@http.route('/info', methods=['POST'])
@auth.login_required
def update_info():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    website = data.get('website')
    business = data.get('business')
    title = data.get('title')
    zone_uid = data.get('zone_uid')
    info = json.loads(data.get('info'))
    h = HTTP.get_item_by_uid(uid=uid)
    with db.auto_commit():
        h.update(website=website, title=title, business=business, zone_uid=zone_uid, info=info)
    return Success()


@http.route('', methods=['POST'])
@auth.login_required
def save_info():
    data = request.get_json(silent=True)
    website = data.get('website')
    title = data.get('title')
    business = data.get('business')
    zone_uid = data.get('zone_uid')
    info = json.loads(data.get('info'))
    with db.auto_commit():
        HTTP.save(website=website, title=title, business=business, zone_uid=zone_uid, info=info)
    return Success()


@http.route('/activate', methods=['POST'])
@auth.login_required
def activate():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = HTTP.get_item_by_uid(uid, status=0)
    with db.auto_commit():
        h.activate()
    return Success()


@http.route('/remove', methods=['POST'])
@auth.login_required
def remove():
    data = request.get_json(silent=True)
    uid = data.get('uid')
    h = HTTP.get_item_by_uid(uid)
    with db.auto_commit():
        h.remove()
    return Success()
