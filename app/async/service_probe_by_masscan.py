from app import celery
from datetime import datetime
import subprocess
import os
import shlex
import json
import fcntl
import time


@celery.task(bind=True)
def do_async_scan(self, targets):
    result = {
        "start_time": datetime.utcnow(),
        "end_time": datetime.utcnow(),
        "result": {
            "total": len(targets.split()),
            "failed": 0,
            "details": []
        }
    }

    self.update_state(state="PROGRESS", meta={'progress': 0})

    temp_file = "temp.json"

    scan_cmd = "masscan -p1-65535 --rate 1000 -oJ {} {}".format(temp_file, targets)
    proc = subprocess.Popen(args=shlex.split(scan_cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    flags = fcntl.fcntl(proc.stdout, fcntl.F_GETFL)
    fcntl.fcntl(proc.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    while True:
        time.sleep(1)
        print(p.stdout.read())
        proc = subprocess.Popen(shlex.split(scan_cmd), stdout=subprocess.PIPE)
        self.update_state(state="PROGRESS", meta={'progress': count/len(targets.split())})

        with open(temp_file, 'r') as f:
            for item in json.loads(f.readlines()):

    result["end_time"] = datetime.utcnow()
    return result
