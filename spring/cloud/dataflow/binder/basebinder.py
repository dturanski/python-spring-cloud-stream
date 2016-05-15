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
import abc


class BaseBinder(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.BINDING_PROPERTIES_PREFIX = 'spring.cloud.stream.bindings.'

    @abc.abstractmethod
    def doBindProducer(self, name, properties):
        """Subclasses must provide implementation"""
        return

    @abc.abstractmethod
    def doBindConsumer(self, name, group, properties):
        """Subclasses must provide implementation"""
        return

    def applyPrefix(self, prefix, name):
        return prefix + name;

    def constructDLQName(self, name):
        return name + ".dlq";

    def groupedName(self, name, group):
        groupName = group if group else 'default'
        return '%s.%s' % (name, group)

    def destinationForBindingTarget(self, name, properties):
        return self.__getBindingProperty__(name, 'destination', properties, True)

    def groupForBindingTarget(self, name, properties):
        return self.__getBindingProperty__(name, 'group', properties, False)

    def bindProducer(self, name, properties):
        return self.doBindProducer(name, properties)

    def bindConsumer(self, name, group, properties):
        return self.doBindConsumer(name, group, properties)

    def __getBindingProperty__(self, name, property, properties, required):
        try:
            return properties[self.BINDING_PROPERTIES_PREFIX + name + '.' + property]
        except(KeyError):
            if required:
                raise RuntimeError('Environment does not contain required property \'{0}\''.format(
                self.BINDING_PROPERTIES_PREFIX + name + '.' + property))
            else:
                return None



