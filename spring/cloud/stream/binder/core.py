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


consumer:
   systemEnvironment: {

INSTANCE_INDEX: "0",
spring.cloud.stream.bindings.input.consumer.partitioned: "true",
spring.cloud.stream.instanceCount: "3",
spring.cloud.stream.bindings.input.group: "ticktock",
},

consumer: {
}

producer:

systemEnvironment: {

INSTANCE_INDEX: "0",
spring.cloud.stream.bindings.output.producer.partitionCount: "3",
spring.cloud.stream.bindings.output.producer.partitionKeyExpression: "payload.subString(payload.lastIndexOf(':')+1)",
},

"""
import abc
from spring.cloud.stream.binding import BindingProperties

class BaseBinder(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, env):
        self.env = env
        self.__binding_properties__ = BindingProperties(env)

    def binding_properties(self, channel_name):
        return self.__binding_properties__.binding_properties(channel_name)

    def producer_properties(self, producer_name):
        return self.__binding_properties__.producer_bindings(producer_name)

    def consumer_properties(self, consumer_name):
        return self.__binding_properties__.consumer_bindings(consumer_name)

    def bind_producer(self, name, producer, producer_name='output'):
        return self.__bind_producer__(name, producer, self.producer_properties(producer_name))

    def bind_consumer(self, name, group, consumer, consumer_name='input'):
        return self.__bind_consumer__(name, group, consumer, self.consumer_properties(consumer_name))

    @abc.abstractmethod
    def __bind_producer__(self, name, producer, producer_properties):
        """Subclasses must provide implementation.
           'name' is the logical identity of the message target
           'producer' is the object to be bound. The object will be provided with a send(message) method
           'producer_properties' are the properties for bound to the producer
        """
        return

    @abc.abstractmethod
    def __bind_consumer__(self, name, group, consumer, consumer_properties):
        """Subclasses must provide implementation.
           'name' is the logical identity of the message source
        'group' is the consumer group to which this consumer belongs - subscriptions are shared among consumers
	        in the same group (a None or empty String, must be treated as an anonymous group that doesn't share
	        the subscription with any other consumer)
	    'consumer' is the object to be bound. The object will be proided with a receive(callback) method
	    'consumer_properties' are the properties for bound to the consumer
        """
        return

    def __apply_prefix__(self, prefix, name):
        return prefix + name;

    def __construct__dlq__name(self, name):
        return name + ".dlq";

    def __grouped_name__(self, name, group):
        groupName = group if group else 'default'
        return '%s.%s' % (name, group)



