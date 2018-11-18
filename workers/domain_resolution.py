from app import celery
from datetime import datetime
import dns.resolver
from celery.signals import before_task_publish, task_postrun, task_success
from app.models.tasks import Task
from app.models.assets import Domain
from workers.result import save


@before_task_publish.connect(sender="workers.domain_resolution.worker")
def before(sender=None, headers=None, body=None, properties=None, **kw):
    targets = ' '.join([domain.name for domain in Domain.query.all()])
    task = Task.insert_task_and_return("test", "test", "test", "test", targets)
    body[1]["targets"] = targets
    headers["id"] = task.id


@task_postrun.connect()
def after(sender=None, task_id=None, retval=None, **kw):
    if sender.name == "workers.domain_resolution.worker":
        print(sender.name)
        print(task_id)
        print(retval)
        save.apply_async(args=(retval, task_id))


@celery.task(bind=True)
def worker(self, targets, task_id=None):
    print(worker.request.id)
    targets = "www.baidu.com"
    print(targets.split())
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
        item = {}

        try:
            answer = dns.resolver.query(domain, 'A')
            for i in answer.response.answer:
                item["domain"] = domain
                item["ip"] = [j.address for j in i.items]
                item["error"] = ""
        except Exception as e:
            item["error"] = e.__repr__()
            result["result"]["failed"] += 1

        result["result"]["details"].append(item)
        count += 1
        self.update_state(state="PROGRESS", meta={'progress': count/len(targets.split())})

    result["end_time"] = datetime.utcnow()
    return result
    # save.delay(result, worker.request.id)

