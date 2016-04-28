#!/usr/bin/env python
import os
import pika
import json

class Binding:
    def __init__(self, channel, destination):
        self.channel = channel
        self.destination = destination

    def send(self,message):
        self.channel.basic_publish(exchange=self.destination,
                              routing_key=self.destination,
                              body=message)
class Binder:
    def __init__(self, connection):
        self.connection = connection
    def bindProducer(self, bindingProperties):
        data = json.loads(bindingProperties)
        destination=data['spring.cloud.stream.bindings.output.destination']
        groups=data['spring.cloud.stream.bindings.output.producer.requiredGroups'].split(',')

        channel = self.connection.channel()
        channel.exchange_declare(exchange=destination,
                             type='topic', durable=True)

        for group in groups:
            queueName= destination + '.' + group
            channel.queue_declare(queue=queueName, durable=True)

        return Binding(channel, destination)

### Obtained from the cloudamqp service dashboard
connection = pika.BlockingConnection(
    pika.URLParameters('amqp://xgkwomgl:aIUHpX761b_pnC9tLnbaVOZAyE9s_1mH@fox.rmq.cloudamqp.com/xgkwomgl'))

binding = Binder(connection).bindProducer(os.environ['SPRING_APPLICATION_JSON'])
binding.send('Hello World!')
connection.close()




