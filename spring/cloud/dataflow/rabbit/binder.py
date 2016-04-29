import uuid
from  spring.cloud.dataflow.basebinder import BaseBinder

#TODO: Autobind DLQ
class Binder(BaseBinder):
    def __init__(self, connection):
        BaseBinder.__init__(self)
        self.connection = connection
        self.RABBIT_PROPERTIES_PREFIX = 'spring.cloud.stream.rabbit.'

    def doBindProducer(self, name, properties):
        groups = properties[self.BINDING_PROPERTIES_PREFIX + 'output.producer.requiredGroups'].split(',')
        #TODO: durable passed as property
        #TODO: handle partitioning
        #TODO: Apply prefix to exchange name passed in properties?
        #TODO Non-partitioned routing key = '#'
        channel = self.connection.channel()
        prefix = self.__getRabbitProperty(properties,'prefix')
        exchangeName = self.applyPrefix(prefix, name)

        channel.exchange_declare(exchange=exchangeName,
                             type='topic', durable=True)

        # TODO: Apply prefix to queue name passed in properties?
        for group in groups:
            queueName= exchangeName + '.' + group
            channel.queue_declare(queue=queueName, durable=True)

        return ProducerBinding(channel, name)

    def doBindConsumer(self, name, group, properties):
        baseQueueName = None
        if not group:
                baseQueueName = self.groupedName(name, 'spring-gen.' + uuid.uuid4())
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
        self.channel.basic_consume(callback,
                              queue=self.destination)
        self.channel.start_consuming()
