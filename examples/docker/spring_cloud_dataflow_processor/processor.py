#!/usr/bin/env python
from spring.cloud.dataflow.binder.rabbit import Binder
from spring.cloud.dataflow import dataflowapp, components
from spring.cloud import environment
import pika
import sys
import json

#
# Merge the application properties provided by environment variables, command line args, etc.
#
env = environment.env(sys.argv)

'''Dump the environment just for fun'''
for (k,v) in env.iteritems():
    print ("{0}={1}".format(k,v))

#
# Connect to the Rabbit MQ broker, given by the standard Spring Cloud Dataflow properties 'SPRING_RABBITMQ_HOST' and 'SPRING_RABBITMQ_HOST'
#
connectionUrl = 'amqp://{0}:{1}'.format(env['SPRING_RABBITMQ_HOST'], env['SPRING_RABBITMQ_PORT'])
connection = pika.BlockingConnection(pika.URLParameters(connectionUrl))

processor = components.Processor()
dataflowapp.bind(processor, Binder(connection), env)


print "bindings created."
#
# Provide a callback function to process each message received in the stream.
#
def callback(channel, method, properties, body):
    print(" [x] Received %r" % body, properties)

    data = {}
    data['original'] = body
    data['reversed'] = str(body)[::-1]
    processor.send(json.dumps(data))

#
# Wait for messages
#
try:
    processor.receive(callback)

finally:
   connection.close()
