#!/usr/bin/env python
from spring.cloud.dataflow.rabbit.binder import Binder
from spring.cloud.dataflow import dataflowapp
import pika
import sys

env = dataflowapp.env(sys.argv)

### Obtained from the cloudamqp service dashboard
connection = pika.BlockingConnection(
    pika.URLParameters('amqp://xgkwomgl:aIUHpX761b_pnC9tLnbaVOZAyE9s_1mH@fox.rmq.cloudamqp.com/xgkwomgl'))

binding = Binder(connection).bindProducer(env)
binding.send('Hello World!')
print "sent message!"
connection.close()

