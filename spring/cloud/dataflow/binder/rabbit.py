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

from  spring.cloud.dataflow.binder.basebinder import BaseBinder

# TODO: Autobind DLQ
class Binder(BaseBinder):
    def __init__(self, connection):
        BaseBinder.__init__(self)
        self.connection = connection
        self.RABBIT_PROPERTIES_PREFIX = 'spring.cloud.stream.rabbit.'

    def doBindProducer(self, name, properties):
        groups = properties[self.BINDING_PROPERTIES_PREFIX + 'output.producer.requiredGroups'].split(',')
        # TODO: durable passed as property
        # TODO: handle partitioning
        # TODO: Apply prefix to exchange name passed in properties?
        # TODO Non-partitioned routing key = '#'
        channel = self.connection.channel()
        prefix = self.__getRabbitProperty(properties, 'prefix')
        exchangeName = self.applyPrefix(prefix, name)

        channel.exchange_declare(exchange=exchangeName,
                                 type='topic', durable=True)

        # TODO: Apply prefix to queue name passed in properties?
        for group in groups:
            queueName = exchangeName + '.' + group
            channel.queue_declare(queue=queueName, durable=True)

        return ProducerBinding(channel, name)

    def doBindConsumer(self, name, group, properties):
        baseQueueName = None
        if not group:
            baseQueueName = self.groupedName(name, 'spring-gen.' + str(uuid.uuid4()))
        else:
            baseQueueName = self.groupedName(name, group)

        channel = self.connection.channel()
        prefix = self.__getRabbitProperty(properties, 'prefix')
        exchangeName = self.applyPrefix(prefix, name)
        channel.exchange_declare(exchange=exchangeName,
                                 type='topic', durable=True)

        queueName = self.applyPrefix(prefix, baseQueueName)

        channel.queue_declare(queue=queueName, durable=True)

        return ConsumerBinding(channel, queueName)

    def __getRabbitProperty(self, properties, name):
        try:
            return properties[self.RABBIT_PROPERTIES_PREFIX + name]
        except:
            return ''


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

    def send(self, message):
        self.channel.basic_publish(exchange=self.destination,
                                   routing_key=self.destination,
                                   body=message)


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
