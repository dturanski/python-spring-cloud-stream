"""
Copyright 2016 the original author or authors.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import uuid

from  spring.cloud.stream.binder.core import BaseBinder
from spring.cloud.stream.binding import RabbitBindingProperties

# TODO: Autobind DLQ
class Binder(BaseBinder):

    def __init__(self, connection, env):
        BaseBinder.__init__(self, env)
        self.connection = connection
        self.rabbit_properties = RabbitBindingProperties(env)

    def __bind_producer__(self, name, producer, producer_properties):
        groups = producer_properties['requiredGroups'].split(',')
        # TODO: durable passed as property
        # TODO: handle partitioning
        # TODO: Apply prefix to exchange name passed in properties?
        # TODO Non-partitioned routing key = '#'
        channel = self.connection.channel()
        producer_name = producer_properties['name']
        exchangeName = self.__apply_prefix__(self.rabbit_properties.producer_bindings(producer_name)['prefix'], name)

        channel.exchange_declare(exchange=exchangeName,
                                 type='topic', durable=True)

        # TODO: Apply prefix to queue name passed in properties?
        for group in groups:
            queueName = exchangeName + '.' + group
            # TODO: Handle non durable option
            channel.queue_declare(queue=queueName, durable=True)
            channel.queue_bind(exchange=exchangeName, queue=queueName, routing_key=name)

        producer.send =  ProducerBinding(channel, name).send

    def __bind_consumer__(self, name, group, consumer, consumer_properties):
        baseQueueName = None
        if not group:
            baseQueueName = self.__grouped_name__(name, 'spring-gen.' + str(uuid.uuid4()))
        else:
            baseQueueName = self.__grouped_name__(name, group)

        channel = self.connection.channel()
        consumer_name = consumer_properties['name']
        prefix = self.rabbit_properties.producer_bindings(consumer_name)['prefix']
        exchangeName = self.__apply_prefix__(prefix, name)
        channel.exchange_declare(exchange=exchangeName, type='topic', durable=True)

        queueName = self.__apply_prefix__(prefix, baseQueueName)

        channel.queue_declare(queue=queueName, durable=True)

        channel.queue_bind(exchange=exchangeName, queue=queueName, routing_key='#')

        consumer.receive = ConsumerBinding(channel, queueName).receive

class Binding:
    def __init__(self, channel, destination):
        self.channel = channel
        self.destination = destination

    def unbind(self):
        # TODO: implement
        return


class ProducerBinding(Binding):
    def __init__(self, channel, destination):
        Binding.__init__(self, channel, destination)

    def send(self, message, properties=None):
        self.channel.basic_publish(exchange=self.destination, routing_key=self.destination, body=message,
                                   properties=properties)

class ConsumerBinding(Binding):
    def __init__(self, channel, destination):
        Binding.__init__(self, channel, destination)

    def receive(self, callback):
        self.channel.basic_consume(CallbackWrapper(callback).invoke,
                                   queue=self.destination)
        self.channel.start_consuming()


class CallbackWrapper:
    def __init__(self, callback):
        self.callback = callback

    def invoke(self, channel, method, properties, body):
        self.callback(channel, method, properties, body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
