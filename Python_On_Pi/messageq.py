import pika, os, logging
logging.basicConfig()

url = os.environ.get('CLOUDAMQP_URL','amqp://fnfdxokx:EPwMQFxwqZU4fHV3JY1VgsxXaVBdUsXn@mosquito.rmq.cloudamqp.com/fnfdxokx')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue = 'sesdata')

channel.basic_publish(exchange='',routing_key='sesdata',body='yoyoyo\n')
print("[x] Message sent")
connection.close()