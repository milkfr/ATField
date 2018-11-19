from app import celery
from celery.signals import before_task_publish, task_postrun
from datetime import datetime
import subprocess
import json
import os
from app.models.tasks import Task
from app.models.assets import Host
from workers.result import save


@before_task_publish.connect(sender="workers.port_scan_quick.worker")
def before(sender=None, headers=None, body=None, properties=None, **kw):
    targets = ' '.join([host.name for host in Host.query.all()])
    task = Task.insert_task_and_return("port scan quick", "timed", "", "周期masscan快扫", targets)
    body[1]["targets"] = targets
    headers["id"] = task.id


@task_postrun.connect()
def after(sender=None, task_id=None, retval=None, **kw):
    if sender.name == "workers.port_scan_quick.worker":
        save.apply_async(args=(retval, task_id))


@celery.task(bind=True)
def worker(self, targets, options):
    self.update_state(state="PROGRESS", meta={'progress': "unknown"})
    result = {
        "start_time": datetime.utcnow(),
        "end_time": datetime.utcnow(),
        "result": {
            "total": len(targets.split()),
            "failed": 0,
            "details": []
        }
    }

    temp_file = "masscan.json"
    scan_cmd = "masscan {} -oJ {} {}".format(options, temp_file, targets)
    subprocess.call(scan_cmd, shell=True)

    with open(temp_file, 'r') as f:
        f.readline()  # delete first line '['
        for line in f.readlines():
            if not line.startswith(']'):  # delete last line ']'
                result["result"]["details"].append(json.loads(line[:-2]))  # delete end ','

    if os.path.exists(temp_file):
        os.remove(temp_file)
    self.update_state(state="PROGRESS", meta={'progress': 100})
    result["end_time"] = datetime.utcnow()
    return result