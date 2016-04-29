#!/usr/bin/env python
from spring.cloud.dataflow.rabbit.binder import Binder
from spring.cloud.dataflow import dataflowapp, components

import pika
import sys


env = dataflowapp.env(sys.argv)

### Obtained from the cloudamqp service dashboard
connection = pika.BlockingConnection(
    pika.URLParameters('amqp://xgkwomgl:aIUHpX761b_pnC9tLnbaVOZAyE9s_1mH@fox.rmq.cloudamqp.com/xgkwomgl'))

sink = components.Sink()
dataflowapp.bind(sink,Binder(connection),env)


def callback(channel, method, properties, body):
    print(" [x] Received %r" % body, properties)
    
    channel.basic_ack(delivery_tag=method.delivery_tag)


sink.receive(callback)

connection.close()



