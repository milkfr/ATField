from celery import Task
from app import celery
from celery.signals import before_task_publish, task_success, task_failure, after_task_publish
import uuid
from app.models.tasks import Task


@before_task_publish.connect
def aaa(sender=None, headers=None, body=None, properties=None, **kw):
    print("abcdefg")
    task_id = str(uuid.uuid1())
    print(type(body))
    print(body)
    print(body[0])
    print(task_id)
    headers["id"] = task_id
    # properties['correlation_id'] = task_id

    # task = Task.insert_task_and_return("test", "test", "test", "test", "a b")
    print("xxxxxxxxxxxxxxxxxxxxxx")


@task_success.connect
def bbb(result=None, task_id=None, **kw):
    print(task_id)
    print(result)
    print("bbbbbbbbbbbbbbbbbbbbbb")


@task_failure.connect
def ccc(**kw):
    print("cccccccccccccccccccccc")


@celery.task
def test_task(x, y):
    print(x+y)
    return x+y




