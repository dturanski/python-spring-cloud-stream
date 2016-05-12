#!/usr/bin/env python
from spring.cloud.dataflow.rabbit.binder import Binder
from spring.cloud.dataflow import dataflowapp, components

import pika
import sys


env = dataflowapp.env(sys.argv)

### Obtained from the cloudamqp service dashboard
#connectionUrl = 'amqp://xgkwomgl:aIUHpX761b_pnC9tLnbaVOZAyE9s_1mH@fox.rmq.cloudamqp.com/xgkwomgl'
connectionUrl = 'amqp://localhost:5672'
connection = pika.BlockingConnection(pika.URLParameters(connectionUrl))

sink = components.Sink()
dataflowapp.bind(sink,Binder(connection),env)

def callback(channel, method, properties, body):
    print(" [x] Received %r" % body, properties)

sink.receive(callback)

connection.close()



