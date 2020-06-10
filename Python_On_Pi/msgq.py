# example_consumer.py
import pika, os, time

def pdf_process_function(msg):
#    print(" PDF processing")
#    print(" [x] Received " + str(msg))
#
#    time.sleep(5) # delays for 5 seconds
#    print(" PDF processing finished");
    file_object = open('sample.txt', 'a')
    file_object.write(str(msg,"utf-8"))
    file_object.close()
    print("[x] msg recevied")
    return;


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://fnfdxokx:EPwMQFxwqZU4fHV3JY1VgsxXaVBdUsXn@mosquito.rmq.cloudamqp.com/fnfdxokx')
params = pika.URLParameters(url)
connection = pike.BlockingConnection(params)
#connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.226',
#                                                               port=5627,
#                                                               virtual_host='/',
#                                                               credentials=pika.credentials.PlainCredentials('user','password')))
channel = connection.channel() # start a channel
channel.queue_declare(queue='sesdata') # Declare a queue

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
    pdf_process_function(body)

# set up subscription on the queue
channel.basic_consume('sesdata',
                      callback,
                      auto_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()
