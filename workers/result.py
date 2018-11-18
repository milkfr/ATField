from app import celery
from app.models.tasks import Task
import json


@celery.task
def save(result, id):
    task = Task.query.filter(Task.id == id).first()
    task.update_result(result=json.dumps(result["result"]))
