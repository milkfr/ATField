from . import api_v_1_0
from flask import request, url_for, jsonify
from ..models.assets import Host, Domain, Service
from ..models.tasks import Task
from ..models.web import Application, Plugin, Package
from sqlalchemy import or_


@api_v_1_0.route("/assets/hosts", methods=["GET"])
def host_list():
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


@api_v_1_0.route("/tasks", methods=["GET"])
def task_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    time_type = request.args.get("time_type", "")
    if time_type == "":
        pagination = Task.query.filter(
            or_(Task.func_type.ilike("%{}%".format(key)),
                Task.time_type.ilike("%{}%".format(key)),
                Task.status.ilike("%{}%".format(key)),
                Task.targets.ilike("%{}%".format(key)),
                Task.options.ilike("%{}%".format(key)),
                Task.description.ilike("%{}%".format(key)))).order_by(
            Task.start_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    else:
        pagination = Task.query.filter(Task.time_type == time_type,
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


@api_v_1_0.route("/web/applications")
def application_list():
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


@api_v_1_0.route("/web/packages")
def package_list():
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


@api_v_1_0.route("/web/plugins")
def plugin_list():
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