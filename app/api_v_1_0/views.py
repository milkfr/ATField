from . import api_v_1_0
from flask import request, url_for, jsonify
from ..models.assets import Host, Domain, Service
from ..models.tasks import Task
from ..models.web import Application, Plugin, Package
from sqlalchemy import or_
import json
from app import csrf


@csrf.exempt
@api_v_1_0.route("/assets/host/add", methods=["POST"])
def host_add():
    # 新增主机信息api_host_add
    json_data = request.get_data()
    host_info_list = json.loads(json_data.decode("utf-8"))
    try:
        Host.insert_items(host_info_list)
    except Exception:
        resp = jsonify({"status": "error"})
    else:
        resp = jsonify({"status": "ok"})
    return resp


@csrf.exempt
@api_v_1_0.route("/assets/host/delete", methods=["POST"])
def host_delete():
    # 根据ip删除主机信息api_host_delete
    json_data = request.get_data()
    ips = json.loads(json_data.decode("utf-8"))
    try:
        for ip in ips:
            host = Host.query.filter(Host.ip == ip).first()
            Host.delete_item(host)
    except Exception:
        resp = jsonify({"status": "error"})
    else:
        resp = jsonify({"status": "ok"})
    return resp


@api_v_1_0.route("/assets/hosts", methods=["GET"])
def host_list():
    # 主机列表接口api_host_list
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Host.query.filter(or_(Host.name.ilike("%{}%".format(key)),
                                       Host.description.ilike("%{}%".format(key)),
                                       Host.ip.ilike("%{}%".format(key)))).paginate(
        page=page, per_page=per_page, error_out=False
    )
    items = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("api_v_1_0.host_list", page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for("api_v_1_0.host_list", page=page+1, _external=True)
    return jsonify({
        "items": [{
            "id": item.id,
            "ip": item.ip,
            "name": item.name,
            "description": item.description,
            "status": item.status,
            "domain_list": [domain.name for domain in item.domain_list],
        } for item in items],
        "prev": prev,
        "next": next,
        "count": pagination.total,
    })


@api_v_1_0.route("/assets/services", methods=["GET"])
def service_list():
    # 服务列表接口api_service_list
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Service.query.filter(or_(Service.name.ilike("%{}%".format(key)),
                                          Service.description.ilike("%{}%".format(key)),
                                          Service.port.ilike("%{}%".format(key)),
                                          Service.tunnel.ilike("%{}%".format(key)),
                                          Service.protocol.ilike("%{}%".format(key)),
                                          Service.service.ilike("%{}%".format(key)))).paginate(
        page=page, per_page=per_page, error_out=False
    )
    items = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("api_v_1_0.service_list", page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for("api_v_1_0.service_list", page=page+1, _external=True)
    return jsonify({
        "items": [{
            "id": item.id,
            "port": item.port,
            "tunnel": item.tunnel,
            "protocol": item.protocol,
            "state": item.state,
            "service": item.service,
            "name": item.name,
            "description": item.description,
            "host": item.host.ip,
        } for item in items],
        "prev": prev,
        "next": next,
        "count": pagination.total,
    })


@api_v_1_0.route("/assets/domains", methods=["GET"])
def domain_list():
    # 域名列表接口api_domain_list
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=10)
    key = request.args.get("key", "")
    pagination = Domain.query.filter(or_(Domain.name.ilike("%{}%".format(key)),
                                         Domain.description.ilike("%{}%".format(key)),)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    items = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("api_v_1_0.domain_list", page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for("api_v_1_0.domain_list", page=page+1, _external=True)
    return jsonify({
        "items": [{
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "host_list": [host.ip for host in item.host_list]
        } for item in items],
        "prev": prev,
        "next": next,
        "count": pagination.total,
    })


@csrf.exempt
@api_v_1_0.route("/assets/domain/add", methods=["POST"])
def domain_add():
    # 新增域名信息api_domain_add
    json_data = request.get_data()
    domain_info_list = json.loads(json_data.decode("utf-8"))
    try:
        Domain.insert_items(domain_info_list)
    except Exception:
        resp = jsonify({"status": "error"})
    else:
        resp = jsonify({"status": "ok"})
    return resp


@csrf.exempt
@api_v_1_0.route("/assets/domain/delete", methods=["POST"])
def domain_delete():
    # 根据域名删除域名信息api_domain_delete
    json_data = request.get_data()
    doamins = json.loads(json_data.decode("utf-8"))
    try:
        for name in doamins:
            domain = Domain.query.filter(Domain.name == name).first()
            Domain.delete_item(domain)
    except Exception:
        resp = jsonify({"status": "error"})
    else:
        resp = jsonify({"status": "ok"})
    return resp


@api_v_1_0.route("/tasks", methods=["GET"])
def task_list():
    # 任务列表接口api_task_list
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Task.query.filter(
        or_(Task.func_type.ilike("%{}%".format(key)),
            Task.time_type.ilike("%{}%".format(key)),
            Task.status.ilike("%{}%".format(key)),
            Task.targets.ilike("%{}%".format(key)),
            Task.options.ilike("%{}%".format(key)),
            Task.description.ilike("%{}%".format(key)))).order_by(
        Task.start_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("api_v_1_0.domain_list", page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for("api_v_1_0.domain_list", page=page+1, _external=True)
    return jsonify({
        "items": [{
            "id": item.id,
            "start_time": item.start_time,
            "end_time": item.end_time,
            "status": item.status,
            "func_type": item.func_type,
            "time_type": item.time_type,
            "description": item.description,
            "targets": item.targets,
            "options": item.options,
            "result": item.result,
        } for item in items],
        "prev": prev,
        "next": next,
        "count": pagination.total,
    })


@api_v_1_0.route("/task/new", methods=["POST"])
def task_new():
    json_data = request.get_data()
    task_info = json.loads(json_data.decode("utf-8"))
    try:
        task = Task.insert_task_and_return(task_info["data"]["func_type"],
                                           task_info["data"]["time_type"],
                                           task_info["data"]["options"],
                                           task_info["data"]["description"],
                                           task_info["data"]["target"])
    except Exception:
        resp = jsonify({"status": "err"})
    else:
        resp = jsonify({"status": "ok", "id": task.id})
    return resp


@api_v_1_0.route("/task/result", methods=["POST"])
def task_result():
    json_data = request.get_data()
    task_info = json.loads(json_data.decode("utf-8"))
    try:
        task = Task.query.filter(Task.id == task_info["id"])
        task.update_result(task_info["result"], task_info["start_time"], task_info["end_time"])
    except Exception:
        resp = jsonify({"status": "err"})
    else:
        resp = jsonify({"status": "ok"})
    return resp



@api_v_1_0.route("/web/applications", methods=["GET"])
def application_list():
    # 应用列表接口api_application_list
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Application.query.filter(Application.name.ilike("%{}%".format(key)),
                                          Application.description.ilike("%{}%".format(key))).paginate(
        page=page, per_page=per_page, error_out=False
    )

    items = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("api_v_1_0.domain_list", page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for("api_v_1_0.domain_list", page=page+1, _external=True)
    return jsonify({
        "items": [{
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "plugin_list": [{"id": plugin.id, "name": plugin.name} for plugin in item.plugin_list],
        } for item in items],
        "prev": prev,
        "next": next,
        "count": pagination.total,
    })


@api_v_1_0.route("/web/packages", methods=["GET"])
def package_list():
    # 报文列表接口api_package_list
    application_id = request.args.get("application_id", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Package.query.filter(Package.application_id == application_id,
                                      Package.entrance.ilike("%{}%".format(key)),
                                      Package.remarks.ilike("%{}%".format(key))).paginate(
        page=page, per_page=per_page, error_out=False
    )
    items = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("api_v_1_0.domain_list", page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for("api_v_1_0.domain_list", page=page+1, _external=True)
    return jsonify({
        "items": [{
            "id": item.id,
            "entrance": item.entrance,
            "path": item.path,
            "method": item.method,
            "status": item.status,
            "request": item.request,
            "response": item.response,
            "remarks": item.remarks,
            "update_time": item.update_time,
        } for item in items],
        "prev": prev,
        "next": next,
        "count": pagination.total,
    })


@api_v_1_0.route("/web/plugins", methods=["GET"])
def plugin_list():
    # 插件列表接口api_plugin_list
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Plugin.query.filter(Plugin.name.ilike("%{}%".format(key)),
                                     Plugin.description.ilike("%{}%".format(key))).paginate(
        page=page, per_page=per_page, error_out=False
    )
    items = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("api_v_1_0.domain_list", page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for("api_v_1_0.domain_list", page=page+1, _external=True)
    return jsonify({
        "items": [{
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "content": item.content,
            "application_list": [{"id": application.id, "name": application.name} for application in item.application_list],
        } for item in items],
        "prev": prev,
        "next": next,
        "count": pagination.total,
    })