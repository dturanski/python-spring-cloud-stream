#!/usr/bin/env python
from spring.cloud.stream.binder.rabbit import Binder
from spring.cloud.stream import components
from spring.cloud import environment, cf

import pika
import sys

env = environment.env(sys.argv)

'''Dump the environment just for fun'''
for (k,v) in env.iteritems():
    print ("{0}={1}".format(k,v))

connection = None

app = cf.App(env)

'''start a thread to listen on the health check endpoint. Another option is to disable health checks'''
health_check = app.start_health_check()

try:

    '''Get service info from VCAP_SERVICES'''
    connectionUrl = app.service('rabbit')['credentials']['uri']
    connection = pika.BlockingConnection(pika.URLParameters(connectionUrl))

    sink = components.Sink()
    sink.bind(Binder(connection), env)

    def callback(channel, method, properties, body):
      print(" [x] Received %r" % body, properties)

    print "Listening for messages..."

    sink.receive(callback)
finally:
    if (connection) :
        connection.close()
    health_check.terminate()


