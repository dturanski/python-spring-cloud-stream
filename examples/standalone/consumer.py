#!/usr/bin/env python
import sys

import pika

from spring.cloud.stream import streamapp, components
from spring.cloud.stream.binder.rabbit import Binder
from spring.cloud import environment

env = environment.env(sys.argv)
#
# If deployed using Spring Cloud Dataflow, or you want to set these environment variables, use this connection String
#connectionUrl = 'amqp://{0}:{1}'.format(env['SPRING_RABBITMQ_HOST'],env['SPRING_RABBITMQ_PORT'])
#

connectionUrl = 'amqp://localhost:5672'
connection = pika.BlockingConnection(pika.URLParameters(connectionUrl))

sink = components.Sink()
sink.bind(Binder(connection), env)

def callback(channel, method, properties, body):
    print(" [x] Received %r" % body, properties)

sink.receive(callback)

connection.close()



