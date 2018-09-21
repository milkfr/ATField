from app import celery
from app.models.tasks import Task
import json
from celery import chain
from . import domain_resolution
from . import service_probe_by_nmap


@celery.task
def save_scan_result(result, task_id):
    task = Task.query.filter(Task.id == task_id).first()
    task.update_result(result=json.dumps(result["result"]),
                       start_time=result["start_time"], end_time=result["end_time"])
    # send mail


def do_scan_task(func_type, time_type, targets, description):
    task = Task.insert_task_and_return(func_type=func_type, time_type=time_type,
                                       targets=targets, description=description)
    task.update_process(Task.STATUS_RUNNING)
    if func_type == Task.FUNC_TYPE_DOMAIN_RESOLUTION:
        chain(domain_resolution.do_async_scan.signature(args=(targets,), task_id=task.id),
              save_scan_result.s(task.id))()
    elif func_type == Task.FUNC_TYPE_SERVICE_PROBE_BY_NMAP:
        chain(service_probe_by_nmap.do_async_scan.signature(args=(targets,), task_id=task.id),
              save_scan_result.s(task.id))()

