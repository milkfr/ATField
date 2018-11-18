from flask import request, render_template
from sqlalchemy import or_
from . import tasks
from .forms import TaskInfoForm
from ..models.tasks import Task


@tasks.route("/list", methods=["GET"])
def task_list():
    # 任务列表查看
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
    return render_template("tasks/list.html", pagination=pagination, url="tasks.task_list",
                           kwargs={"per_page": per_page, "key": key})


@tasks.route("/info", methods=["GET"])
def info():
    # 任务详情查看
    task_id = request.args.get("id", "", type=str)
    task = Task.query.filter(Task.id == task_id).first()
    form = TaskInfoForm()
    form.func_type.data = task.func_type
    form.time_type.data = task.time_type
    form.description.data = task.description
    form.options.data = task.options
    form.targets.data = task.targets
    # if task.status == Task.STATUS_RUNNING:
    #     if task.func_type == Task.FUNC_TYPE_DOMAIN_RESOLUTION:
    #         from app.async import domain_resolution
    #         progress = domain_resolution.do_async_scan.AsyncResult(task.id)
    #         form.status.data = progress.info.get("progress")
    #     elif task.func_type == Task.FUNC_TYPE_SERVICE_PROBE_BY_NMAP:
    #         from app.async import service_probe_by_nmap
    #         progress = service_probe_by_nmap.do_async_scan.AsyncResult(task.id)
    #         form.status.data = progress.info.get("progress")
    #     elif task.func_type == Task.FUNC_TYPE_SERVICE_PROBE_BY_MASSCAN:
    #         from app.async import service_probe_by_masscan
    #         progress = service_probe_by_masscan.do_async_scan.AsyncResult(task.id)
    #         form.status.data = progress.info.get("progress")
    # else:
    #     form.status.data = task.status
    form.start_time.data = task.start_time
    form.end_time.data = task.end_time
    form.result.data = task.result
    return render_template("tasks/info.html", form=form)
