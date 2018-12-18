from app import celery
from celery.signals import before_task_publish, task_postrun
from app.models.tasks import Task
from app.models.assets import Domain
from workers.result import save
import pika
from config import config
import json


@before_task_publish.connect(sender="workers.awvs.worker")
def before(sender=None, headers=None, body=None, properties=None, **kw):
    targets = ' '.join([domain.name for domain in Domain.query.all()])
    task = Task.insert_task_and_return("awvs", "timed", "awvs周期扫描", targets)
    body[1]["targets"] = "127.0.0.1:8088"
    body[1]["options"] = "do scan"
    headers["id"] = task.id


@task_postrun.connect()
def after(sender=None, task_id=None, retval=None, **kw):
    if sender.name == "workers.awvs.worker":
        pass
        # save.apply_async(args=(retval, task_id))


@celery.task(bind=True)
def worker(self, targets, options):
    print(" [x] start Send {} {}", options, targets)
    connection = pika.BlockingConnection(pika.URLParameters(config.CELERY_BROKER_URL))

    channel = connection.channel()

    channel.exchange_declare(
        exchange="awvs",
        exchange_type="direct",
        durable=True,
    )

    channel.queue_declare(
        queue="awvs",
        durable=True,
    )

    channel.queue_bind(
        queue="awvs",
        exchange="awvs",
        routing_key="awvs",
    )
    channel.basic_publish(
        exchange="awvs",
        routing_key="awvs",
        body=json.dumps({"option": options, "targets": targets})
    )
    print(" [x] Send {} {}".format(options, targets))
    connection.close()
