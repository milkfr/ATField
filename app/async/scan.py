from app import celery
from app.models.tasks import Task
import json
from celery import chain
from . import domain_resolution
from . import service_probe_by_nmap
from . import service_probe_by_masscan


@celery.task
def save_scan_result(result, task_id):
    task = Task.query.filter(Task.id == task_id).first()
    task.update_result(result=json.dumps(result["result"]),
                       start_time=result["start_time"], end_time=result["end_time"])
    # send mail


@celery.task
def do_scan_task(func_type, time_type, options, targets, description):
    task = Task.insert_task_and_return(func_type=func_type, time_type=time_type, options=options,
                                       targets=targets, description=description)
    task.update_process(Task.STATUS_RUNNING)
    if func_type == Task.FUNC_TYPE_DOMAIN_RESOLUTION:
        chain(domain_resolution.do_async_scan.signature(args=(targets,), task_id=task.id),
              save_scan_result.s(task.id))()
    elif func_type == Task.FUNC_TYPE_SERVICE_PROBE_BY_NMAP:
        chain(service_probe_by_nmap.do_async_scan.signature(args=(targets, options,), task_id=task.id),
              save_scan_result.s(task.id))()
    elif func_type == Task.FUNC_TYPE_SERVICE_PROBE_BY_MASSCAN:
        chain(service_probe_by_masscan.do_async_scan.signature(args=(targets, options,), task_id=task.id),
              save_scan_result.s(task.id))()


# @.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )

