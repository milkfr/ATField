import pika
import json

connection = pika.BlockingConnection(pika.URLParameters('amqp://rabbitmq:rabbitmq@127.0.0.1:5672/atfield'))

channel = connection.channel()

channel.exchange_declare(
    exchange="nessus",
    exchange_type="direct",
    durable=True,
)

channel.queue_declare(
    queue="nessus",
    durable=True,
)

channel.queue_bind(
    queue="nessus",
    exchange="nessus",
    routing_key="nessus",
)


def callback(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    print(json.loads(body.decode("utf-8")))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    callback,
    queue="nessus",
)

channel.start_consuming()