from flask import request, render_template, redirect, url_for
from sqlalchemy import or_
from . import tasks
from .forms import TaskNewForm, TaskTargetForm, TaskInfoForm
from ..models.tasks import Task
from ..models.probe import Host, Domain
from ..async.scan import do_async_scan


@tasks.route("/new", methods=["GET", "POST"])
def new():
    new_form = TaskNewForm()
    target_form = TaskTargetForm()
    if new_form.next.data and new_form.validate_on_submit():
        target_form.func_type.data = new_form.func_type.data
        target_form.command.data = new_form.command.data
        target_form.description.data = new_form.description.data
        if new_form.func_type.data == "domain resolution":
            target_form.targets.choices = [(domain.name, domain.name) for domain in Domain.query.all()]
        elif new_form.func_type.data == "service probe" or new_form.func_type.data == "host scan":
            target_form.targets.choices = [(host.ip, host.ip) for host in Host.query.all()]
        return render_template("tasks/new.html", form=target_form)
    elif target_form.submit.data:
        target_form.targets.choices = [(domain.name, domain.name) for domain in Domain.query.all()]
        if target_form.validate_on_submit():
            do_async_scan.apply_async(args=(target_form.func_type.data, "once", target_form.command.data,
                                            ' '.join(target_form.targets.data), target_form.description.data))
            # task = Task.insert_task_and_return(
            #     func_type=target_form.func_type.data, time_type="once", command=target_form.command.data,
            #     description=target_form.description.data, targets=' '.join(target_form.targets.data))
            # celery_data = [{
            #     "func_type": task.func_type,
            #     "command": task.command,
            #     "targets": task.targets,
            # }]
            # celery_task = do_async_domain_resolution.apply_async(celery_data)
            # task.update_process(celery_task.id, status="running")
            return redirect(url_for("tasks.once_list"))

    return render_template("tasks/new.html", form=new_form)


# @celery.task(bind=True)
# def do_async_domain_resolution(self, task):
#     if task["func_type"] == "domain resolution":
#         import dns.resolver
#         count = 0
#         for domain in task["targets"].split():
#             count += 1
#             self.update_state(state='PROGRESS',
#                               meta={'current': count, 'total': 100,
#                                     'status': ""})
#             try:
#                 answer = dns.resolver.query(domain, 'A')
#                 for i in answer.response.answer:
#                     print([j.address for j in i.items])
#             except Exception as e:
#                 print(e)
#             import time
#             time.sleep(3)
#     return {'current': 100, 'total': 100, 'status': 'Task completed!',
#             'result': 42}


@tasks.route("/timed_list")
def timed_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Task.query.filter(Task.time_type != "once",
                                   or_(Task.func_type.ilike("%{}%".format(key)),
                                       Task.time_type.ilike("%{}%".format(key)),
                                       Task.command.ilike("%{}%".format(key)),
                                       Task.status.ilike("%{}%".format(key)),
                                       Task.targets.ilike("%{}%".format(key)),
                                       Task.description.ilike("%{}%".format(key)))).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("tasks/timed_list.html", pagination=pagination, url="tasks.timed_list")


@tasks.route("/once_list")
def once_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    key = request.args.get("key", "")
    pagination = Task.query.filter(Task.time_type == "once",
                                   or_(Task.func_type.ilike("%{}%".format(key)),
                                       Task.time_type.ilike("%{}%".format(key)),
                                       Task.command.ilike("%{}%".format(key)),
                                       Task.status.ilike("%{}%".format(key)),
                                       Task.targets.ilike("%{}%".format(key)),
                                       Task.description.ilike("%{}%".format(key)))).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("tasks/once_list.html", pagination=pagination, url="tasks.once_list")


@tasks.route("/info")
def info():
    task_id = request.args.get("id", "", type=str)
    task = Task.query.filter(Task.id == task_id).first()
    form = TaskInfoForm()
    form.func_type.data = task.func_type
    form.time_type.data = task.time_type
    form.command.data = task.command
    form.description.data = task.description
    form.targets.data = task.targets
    form.status.data = task.status
    form.start_time.data = task.start_time
    form.end_time.data = task.end_time
    form.result.data = task.result
    return render_template("tasks/info.html", form=form)
