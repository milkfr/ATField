from app import celery
from datetime import datetime
import dns.resolver


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
    count = 0
    self.update_state(state="PROGRESS", meta={'progress': count/len(targets.split())})
    for domain in targets.split():
        item = {}

        try:
            answer = dns.resolver.query(domain, 'A')
            for i in answer.response.answer:
                import time
                time.sleep(5)
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
