from sqlalchemy import or_

from flask import request, render_template, redirect, url_for
from . import assets
from .forms import HostUpdateForm, DomainUpdateForm, ServiceUpdateForm
from ..models.assets import Host, Domain, Service


@assets.route("/host/list", methods=["GET"])
def host_list():
    # 主机资产查看
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Host.query.filter(or_(Host.name.ilike("%{}%".format(key)),
                                       Host.description.ilike("%{}%".format(key)),
                                       Host.ip.ilike("%{}%".format(key)))).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("assets/host_list.html", pagination=pagination, url="assets.host_list",
                           kwargs={"per_page": per_page, "key": key})


@assets.route("/host/update", methods=["GET", "POST"])
def host_update():
    # 主机资产信息修改
    host_id = request.args.get("id", "", type=str)
    host = Host.query.filter(Host.id == host_id).first()
    form = HostUpdateForm(host)
    if form.validate_on_submit():
        host.update_info(name=form.name.data, description=form.description.data)
        return redirect(url_for("assets.host_list"))
    form.ip.data = host.ip
    form.status.data = host.status
    form.name.data = host.name
    form.description.data = host.description
    return render_template("assets/host_update.html", form=form)


@assets.route("/service/list", methods=["GET"])
def service_list():
    # 服务资产查看
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
    return render_template("assets/service_list.html", pagination=pagination, url="assets.service_list",
                           kwargs={"per_page": per_page, "key": key})


@assets.route("/service/update", methods=["GET", "POST"])
def service_update():
    # 服务资产信息修改
    service_id = request.args.get("id", "", type=str)
    service = Service.query.filter(Service.id == service_id).first()
    form = ServiceUpdateForm()
    if form.validate_on_submit():
        service.update_info(name=form.name.data, description=form.description.data)
        return redirect(url_for("assets.service_list"))
    form.port.data = service.port
    form.tunnel.data = service.tunnel
    form.protocol.data = service.protocol
    form.state.data = service.state
    form.host.data = service.host
    form.name.data = service.name
    form.description.data = service.description
    return render_template("assets/service_update.html", form=form)


@assets.route("/domain/list", methods=["GET"])
def domain_list():
    # 域名资产查看
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Domain.query.filter(or_(Domain.name.ilike("%{}%".format(key)),
                                       Domain.description.ilike("%{}%".format(key)),)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("assets/domain_list.html", pagination=pagination, url="assets.domain_list",
                           kwargs={"per_page": per_page, "key": key})


@assets.route("/domain/update", methods=["GET", "POST"])
def domain_update():
    # 域名资产信息修改
    domain_id = request.args.get("id", "", type=str)
    domain = Domain.query.filter(Domain.id == domain_id).first()
    form = DomainUpdateForm(domain)
    if form.validate_on_submit():
        domain.update_info(description=form.description.data)
        return redirect(url_for("assets.domain_list"))
    form.name.data = domain.name
    form.description.data = domain.description
    return render_template("assets/domain_update.html", form=form)
