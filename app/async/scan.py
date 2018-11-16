from app import celery
from app.models.tasks import Task
import json
from celery import chain
from celery.signals import before_task_publish, task_success, task_failure
from . import domain_resolution
from . import service_probe_by_nmap
from . import service_probe_by_masscan
import uuid


@before_task_publish.connect
def aaa(sender=None, headers=None, body=None, properties=None, **kw):
    task_id = uuid.uuid1()
    print(task_id)
    properties['correlation_id']: task_id
    print("xxxxxxxxxxxxxxxxxxxxxx")


@task_success.connect
def bbb(**kw):
    print("bbbbbbbbbbbbbbbbbbbbbb")
    pass


@task_failure.connect
def ccc(**kw):
    print("cccccccccccccccccccccc")
    pass


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
