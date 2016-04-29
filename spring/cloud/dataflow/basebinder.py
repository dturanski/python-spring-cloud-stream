#!/usr/bin/env python
import abc

class BaseBinder(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.BINDING_PROPERTIES_PREFIX = 'spring.cloud.stream.bindings.'

    @abc.abstractmethod
    def doBindProducer(self,name, properties):
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

    def groupedName(self,group,name):
        groupName =  group if group else 'default'
        return '%s.%s' %(groupName, name)

    def destinationForBindingTarget(self, name, properties):
        return properties[self.BINDING_PROPERTIES_PREFIX + name + '.destination']

    def groupForBindingTarget(self, name, properties):
        return properties[self.BINDING_PROPERTIES_PREFIX + name + '.group']
    def bindProducer(self, name, properties):
        return self.doBindProducer(name, properties)

    def bindConsumer(self, name, group, properties):
        return self.doBindConsumer(name, group, properties)








