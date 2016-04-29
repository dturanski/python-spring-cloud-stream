from  spring.cloud.dataflow.basebinder import BaseBinder
#TODO: Autobind DLQ
class Binder(BaseBinder):
    def __init__(self, connection):
        self.connection = connection

    def doBindProducer(self, name, properties):
        groups = properties['spring.cloud.stream.bindings.output.producer.requiredGroups'].split(',')
        #TODO: durable passed as property
        #TODO: handle partitioning
        #TODO: Apply prefix to exchange name passed in properties?
        #TODO Non-partitioned routing key = '#'
        channel = self.connection.channel()

        exchangeName = self.applyPrefix('', name)

        channel.exchange_declare(exchange=exchangeName,
                             type='topic', durable=True)

        # TODO: Apply prefix to queue name passed in properties?
        for group in groups:
            queueName= name + '.' + group
            channel.queue_declare(queue=queueName, durable=True)

        return Binding(channel, name)

    def doBindConsumer(self, name, group, properties):
        #TODO: implement
        return


class Binding:
    def __init__(self, channel, destination):
        self.channel = channel
        self.destination = destination

    def send(self,message):
        self.channel.basic_publish(exchange=self.destination,
                              routing_key=self.destination,
                              body=message)
    def unbind(self):
        # TODO: implement
        return