import os
import json
import components

def env(args):
    environment = __parseSpringApplicationJson()
    for arg in args:
        if (arg.startswith('--')):
            (key,value)=arg.split("=")
            key = key.replace('--','')
            environment[key]=value
    return environment

def bind(target, binder, properties):
    for name, bindingTarget in __getBindingTargets(target).iteritems():
        if bindingTarget.type == 'output':
            destination = binder.destinationForBindingTarget(name, properties)
            binding = binder.bindProducer(destination, properties)
            bindingTarget.send = binding.send

        elif bindingTarget.type == 'input':
            group = binder.groupForBindingTarget(name, properties)
            destination =binder.destinationForBindingTarget(name, properties)
            binding = binder.bindConsumer(destination, group, properties)
            bindingTarget.receive = binding.receive

def __getBindingTargets(object):
    bindingTargets = {}
    if object.__class__ == components.BindingTarget:
        bindingTargets[object.name] = object.type
    for (k, v) in object.__dict__.iteritems():
        if v.__class__ == components.BindingTarget:
            bindingTargets[k] = v
    return bindingTargets


def __parseSpringApplicationJson():
    environment={}
    try:
        springApplicationJson=os.environ['SPRING_APPLICATION_JSON']
        if (springApplicationJson):
            environment=json.loads(springApplicationJson)
    except:
        pass
    return environment
