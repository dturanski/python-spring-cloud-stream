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

class BindingProperties:
    BINDING_PROPERTIES_PREFIX = 'spring.cloud.stream.bindings.'
    def __init__(self,properties):
        self.properties=properties


class BaseBinder(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __bind_producer__(self, name, properties):
        """Subclasses must provide implementation"""
        return

    @abc.abstractmethod
    def __bind_consumer__(self, name, group, properties):
        """Subclasses must provide implementation"""
        return

    def __apply_prefix__(self, prefix, name):
        return prefix + name;

    def __construct__dlq__name(self, name):
        return name + ".dlq";

    def __grouped_name__(self, name, group):
        groupName = group if group else 'default'
        return '%s.%s' % (name, group)

    def __destination_for_binding_target__(self, name, properties):
        return self.__getBindingProperty__(name, 'destination', properties, True)

    def __group_for_binding_target__(self, name, properties):
        return self.__getBindingProperty__(name, 'group', properties, False)

    def bind_producer(self, name, properties):
        return self.__bind_producer__(name, properties)

    def bind_consumer(self, name, group, properties):
        return self.__bind_consumer__(name, group, properties)

    def __getBindingProperty__(self, name, property, properties, required):
        try:
            return properties[BaseBinder.BINDING_PROPERTIES_PREFIX + name + '.' + property]
        except(KeyError):
            if required:
                raise RuntimeError('Environment does not contain required property \'{0}\''.format(
                    BaseBinder.BINDING_PROPERTIES_PREFIX + name + '.' + property))
            else:
                return None



