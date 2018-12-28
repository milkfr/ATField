from app import celery
from celery.signals import before_task_publish, task_postrun
from app.models.tasks import Task
from app.models.assets import Host
from app.models.assets import Service
from sqlalchemy import and_
import pika
from config import config
import json


@before_task_publish.connect(sender="workers.amqp.worker")
def before(sender=None, headers=None, body=None, properties=None, **kw):
    task_name = body[1]["task"]
    options = body[1]["options"]
    targets = None
    task = None
    if task_name == "nessus":
        targets = ' '.join([host.ip for host in Host.query.all()])
    elif task_name == "awvs":
        targets = Service.query.filter(and_(Service.state != "closed",
                                            Service.service == "http", Service.service == "https")).all()
        targets = ' '.join(["{}://{}:{}".format(target.service, target.host.ip, target.port) for target in targets])
    if options == "do scan":
        task = Task.insert_task_and_return(task_name, "timed", "{}周期扫描".format(task_name), targets)
    elif options == "get report":
        task = Task.query.filter(Task.func_type == "port monitor").order_by(Task.start_time.desc()).first()
        task.update_result(result="ok")
    print(body[1])
    body[1]["targets"] = targets
    headers["id"] = task.id


@task_postrun.connect()
def after(sender=None, task_id=None, retval=None, **kw):
    if sender.name == "workers.amqp.worker":
        pass
        # save.apply_async(args=(retval, task_id))


@celery.task(bind=True)
def worker(self, task, targets, options):
    publishing(name=task, targets=targets, options=options)


def publishing(name, options, targets):
    print(" [x] start Send {} {} {}", name, options, targets)
    connection = pika.BlockingConnection(pika.URLParameters(config.CELERY_BROKER_URL))

    channel = connection.channel()

    channel.exchange_declare(
        exchange=name,
        exchange_type="direct",
        durable=True,
    )

    channel.queue_declare(
        queue=name,
        durable=True,
    )

    channel.queue_bind(
        queue=name,
        exchange=name,
        routing_key=name,
    )
    channel.basic_publish(
        exchange=name,
        routing_key=name,
        body=json.dumps({"options": options, "targets": targets})
    )
    print(" [x] Send {} {} {}".format(name, options, targets))
    connection.close()
