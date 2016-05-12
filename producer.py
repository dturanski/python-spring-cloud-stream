#!/usr/bin/env python
import sys

import pika

from spring.cloud.dataflow import dataflowapp, components
from spring.cloud.dataflow.binder.rabbit import Binder

env = dataflowapp.env(sys.argv)

#
# If deployed using Spring Cloud Dataflow, or you want to set these environment variables, use this connection String
#connectionUrl = 'amqp://{0}:{1}'.format(env['SPRING_RABBITMQ_HOST'],env['SPRING_RABBITMQ_PORT'])
#
connectionUrl = 'amqp://localhost:5672'
connection = pika.BlockingConnection(pika.URLParameters(connectionUrl))

source = components.Source()
dataflowapp.bind(source,Binder(connection),env)

source.send('Hello World!')

print "sent message!"
connection.close()



