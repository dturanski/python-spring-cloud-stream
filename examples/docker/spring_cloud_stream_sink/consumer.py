#!/usr/bin/env python
from spring.cloud.stream.binder.rabbit import Binder
from spring.cloud.stream import streamapp, components
from spring.cloud import environment
import pika
import sys

#
# Merge the application properties provided by environment variables, command line args, etc.
#
env = environment.env(sys.argv)

#
# Connect to the Rabbit MQ broker, given by the standard Spring Cloud Dataflow properties 'SPRING_RABBITMQ_HOST' and 'SPRING_RABBITMQ_HOST'
#
connectionUrl = 'amqp://{0}:{1}'.format(env['SPRING_RABBITMQ_HOST'],env['SPRING_RABBITMQ_PORT'])
connection = pika.BlockingConnection(pika.URLParameters(connectionUrl))

#
# Declare a sink and bind it to Rabbit MQ transport using required Spring Cloud Stream binding properties provided by the Dataflow server
#
sink = components.Sink()
streamapp.bind(sink, Binder(connection), env)

#
# Provide a callback function to process each message received in the stream.
#
def callback(channel, method, properties, body):
    print(" [x] Received %r" % body, properties)

#
# Wait for messages
#
try:
    sink.receive(callback)

finally:
    connection.close()



