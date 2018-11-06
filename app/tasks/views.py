from flask import request, render_template, redirect, url_for
from sqlalchemy import or_
from . import tasks
from .forms import TaskNewForm, TaskTargetForm, TaskInfoForm
from ..models.tasks import Task
from ..models.assets import Host, Domain
from ..async.scan import do_scan_task


@tasks.route("/new", methods=["GET", "POST"])
def new():
    new_form = TaskNewForm()
    target_form = TaskTargetForm()
    if new_form.next.data and new_form.validate_on_submit():
        target_form.func_type.data = new_form.func_type.data
        target_form.description.data = new_form.description.data
        target_form.options.data = new_form.options.data
        if new_form.func_type.data in [Task.FUNC_TYPE_DOMAIN_RESOLUTION]:
            target_form.targets.choices = [(domain.name, domain.name) for domain in Domain.query.all()]
        elif new_form.func_type.data in [Task.FUNC_TYPE_SERVICE_PROBE_BY_NMAP, Task.FUNC_TYPE_SERVICE_PROBE_BY_MASSCAN]:
            target_form.targets.choices = [(host.ip, host.ip) for host in Host.query.all()]
        return render_template("tasks/new.html", form=target_form)
    elif target_form.submit.data:
        if target_form.func_type.data in [Task.FUNC_TYPE_DOMAIN_RESOLUTION]:
            target_form.targets.choices = [(domain.name, domain.name) for domain in Domain.query.all()]
        elif target_form.func_type.data in [Task.FUNC_TYPE_SERVICE_PROBE_BY_NMAP,
                                            Task.FUNC_TYPE_SERVICE_PROBE_BY_MASSCAN]:
            target_form.targets.choices = [(host.ip, host.ip) for host in Host.query.all()]
        if target_form.validate_on_submit():
            do_scan_task.apply_async(args=(target_form.func_type.data, Task.TIME_TYPE_ONCE,
                                     target_form.options.data, ' '.join(target_form.targets.data),
                                     target_form.description.data))
            return redirect(url_for("tasks.once_list"))

    return render_template("tasks/new.html", form=new_form)


@tasks.route("/timed_list")
def timed_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Task.query.filter(Task.time_type != "once",
                                   or_(Task.func_type.ilike("%{}%".format(key)),
                                       Task.time_type.ilike("%{}%".format(key)),
                                       Task.status.ilike("%{}%".format(key)),
                                       Task.targets.ilike("%{}%".format(key)),
                                       Task.options.ilike("%{}%".format(key)),
                                       Task.description.ilike("%{}%".format(key)))).order_by(
        Task.start_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("tasks/timed_list.html", pagination=pagination, url="tasks.timed_list",
                           kwargs={"per_page": per_page, "key": key})


@tasks.route("/once_list")
def once_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Task.query.filter(Task.time_type == "once",
                                   or_(Task.func_type.ilike("%{}%".format(key)),
                                       Task.time_type.ilike("%{}%".format(key)),
                                       Task.status.ilike("%{}%".format(key)),
                                       Task.targets.ilike("%{}%".format(key)),
                                       Task.options.ilike("%{}%".format(key)),
                                       Task.description.ilike("%{}%".format(key)))).order_by(
        Task.start_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("tasks/once_list.html", pagination=pagination, url="tasks.once_list",
                           kwargs={"per_page": per_page, "key": key})


@tasks.route("/info")
def info():
    task_id = request.args.get("id", "", type=str)
    task = Task.query.filter(Task.id == task_id).first()
    form = TaskInfoForm()
    form.func_type.data = task.func_type
    form.time_type.data = task.time_type
    form.description.data = task.description
    form.options.data = task.options
    form.targets.data = task.targets
    if task.status == Task.STATUS_RUNNING:
        if task.func_type == Task.FUNC_TYPE_DOMAIN_RESOLUTION:
            from app.async import domain_resolution
            progress = domain_resolution.do_async_scan.AsyncResult(task.id)
            form.status.data = progress.info.get("progress")
        elif task.func_type == Task.FUNC_TYPE_SERVICE_PROBE_BY_NMAP:
            from app.async import service_probe_by_nmap
            progress = service_probe_by_nmap.do_async_scan.AsyncResult(task.id)
            form.status.data = progress.info.get("progress")
        elif task.func_type == Task.FUNC_TYPE_SERVICE_PROBE_BY_MASSCAN:
            from app.async import service_probe_by_masscan
            progress = service_probe_by_masscan.do_async_scan.AsyncResult(task.id)
            form.status.data = progress.info.get("progress")
    else:
        form.status.data = task.status
    form.start_time.data = task.start_time
    form.end_time.data = task.end_time
    form.result.data = task.result
    return render_template("tasks/info.html", form=form)
