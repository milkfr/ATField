from . import web
from flask import request, render_template, redirect, url_for
from app.models.web import Application, Package, Plugin
from .forms import ApplicationUpdateForm, PackageUpdateForm, PluginUpdateForm


@web.route("/application/list")
def application_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Application.query.filter(Application.name.ilike("%{}%".format(key)),
                                          Application.description.ilike("%{}%".format(key))).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("web/application_list.html", pagination=pagination, url="web.application_list",
                           kwargs={"per_page": per_page, "key": key})


@web.route("/application/update", methods=["GET", "POST"])
def application_update():
    application_id = request.args.get("id", "", type=str)
    application = Application.query.filter(Application.id == application_id).first()
    form = ApplicationUpdateForm()
    if form.validate_on_submit():
        plugin_id_list = form.plugin.data
        old_plugin_id_list = [plugin.id for plugin in application.plugin_list]
        delete_plugin_list = list(set(old_plugin_id_list).difference(set(plugin_id_list)))
        add_plugin_list = list(set(plugin_id_list).difference(set(old_plugin_id_list)))
        application.update_plugin_by_id(delete_plugin_list, add_plugin_list)
        return redirect(url_for("web.application_list"))
    form.name.data = application.name
    form.description.data = application.description
    form.plugin.data = [plugin.id for plugin in application.plugin_list]
    return render_template("web/application_update.html", form=form)


@web.route("/package/list")
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
    return render_template("web/package_list.html", pagination=pagination, url="web.application_list",
                           kwargs={"per_page": per_page, "key": key, "application_id": application_id})


@web.route("/package/update", methods=["GET", "POST"])
def package_update():
    package_id = request.args.get("id", "", type=str)
    package = Package.query.filter(Package.id == package_id).first()
    form = PackageUpdateForm()
    if form.validate_on_submit():
        package.update_info(request=form.request.data, response=form.request.data, remarks=form.remarks.data)
        return redirect(url_for("web.package_list", application_id=package.application_id))
    form.application.data = package.application
    form.entrance.data = package.entrance
    form.path.data = package.path
    form.method.data = package.method
    form.status.data = package.status
    form.request.data = package.request
    form.response.data = package.response
    form.remarks.data = package.remarks
    return render_template("web/package_update.html", form=form)


@web.route("/plugin/list")
def plugin_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Plugin.query.filter(Plugin.name.ilike("%{}%".format(key)),
                                     Plugin.description.ilike("%{}%".format(key))).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("web/plugin_list.html", pagination=pagination, url="web.plugin_list",
                           kwargs={"per_page": per_page, "key": key})


@web.route("/plugin/update", methods=["GET", "POST"])
def plugin_update():
    plugin_id = request.args.get("id", "", type=str)
    plugin = Plugin.query.filter(Plugin.id == plugin_id).first()
    form = PluginUpdateForm()
    if form.validate_on_submit():
        plugin.update_info(name=form.name.data, description=form.description.data, content=form.description.data)
        return redirect(url_for("web.plugin_list"))
    form.name.data = plugin.name
    form.description.data = plugin.description
    form.content.data = plugin.content.data
    form.application.data = [application.id for application in plugin.application_list]
    return render_template("web/plugin_update.html", form=form)
