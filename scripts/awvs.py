import pika
import json

connection = pika.BlockingConnection(pika.URLParameters('amqp://rabbitmq:rabbitmq@127.0.0.1:5672/atfield'))

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


def callback(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    print(json.loads(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    callback,
    queue="awvs",
)

channel.start_consuming()
