import pika
from config import config


RABBITMQ_URL = config.CELERY_BROKER_URL


def consuming(name, callback):
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))

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

    channel.basic_consume(
        callback,
        queue=name,
    )

    channel.start_consuming()