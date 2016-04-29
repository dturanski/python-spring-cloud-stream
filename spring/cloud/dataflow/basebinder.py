#!/usr/bin/env python
import abc

class BaseBinder(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def doBindProducer(self,destination,groups):
        """Subclasses must provide implementation"""
        return

    def groupedName(self,group,name):
        groupName =  group if group else 'default'
        return '%s.%s' %(name,groupName)

    def bindProducer(self, env):
        # TODO: durable passed as property
        # TODO: handle partitioning
        # TODO: Apply prefix to exchange name passed in properties?
        # TODO Non-partitioned routing key = '#'
        destination = env['spring.cloud.stream.bindings.output.destination']
        groups = env['spring.cloud.stream.bindings.output.producer.requiredGroups']
        return self.doBindProducer(destination,groups)


    def unbind(self):
         # TODO: implement
        return






