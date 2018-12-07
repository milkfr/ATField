from app import celery
from datetime import datetime
import dns.resolver
from celery.signals import before_task_publish, task_postrun
from app.models.tasks import Task
from app.models.assets import Domain
from workers.result import save


@before_task_publish.connect(sender="workers.domain_resolution.worker")
def before(sender=None, headers=None, body=None, properties=None, **kw):
    targets = ' '.join([domain.name for domain in Domain.query.all()])
    task = Task.insert_task_and_return("domain resolution", "timed", "", "周期域名检测", targets)
    body[1]["targets"] = targets
    headers["id"] = task.id


@task_postrun.connect()
def after(sender=None, task_id=None, retval=None, **kw):
    if sender.name == "workers.domain_resolution.worker":
        save.apply_async(args=(retval, task_id))


@celery.task(bind=True)
def worker(self, targets):
    result = {
        "start_time": datetime.utcnow(),
        "end_time": datetime.utcnow(),
        "result": {
            "total": len(targets.split()),
            "failed": 0,
            "details": []
        }
    }
    count = 0
    self.update_state(state="PROGRESS", meta={'progress': count/len(targets.split())})
    for domain in targets.split():
        item = {
            "ip": None,
            "description": "",
            "domain": "",
        }
        try:
            answer = dns.resolver.query(domain, 'A')
            item["domain"] = domain
            for i in answer.response.answer:
                if i.rdtype == 1:
                    item["ip"] = [j.address for j in i.items]
                elif i.rdtype == 5:
                    item["description"] += "CNAME: " + i.name.to_text() + " "
        except Exception as e:
            item["description"] += e.__repr__()
            result["result"]["failed"] += 1

        result["result"]["details"].append(item)
        count += 1
        self.update_state(state="PROGRESS", meta={'progress': count/len(targets.split())})

    result["end_time"] = datetime.utcnow()
    return result
