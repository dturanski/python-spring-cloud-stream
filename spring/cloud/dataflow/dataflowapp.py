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
import os
import json
import socket
import multiprocessing

from spring.cloud.dataflow import components

def env(args):
    environment = os.environ
    environment.update(__parseSpringApplicationJson())

    for arg in args:
        if (arg.startswith('--')):
            (key, value) = arg.split("=")
            key = key.replace('--', '')
            environment[key] = value
    return environment


def bind(target, binder, properties):
    for name, bindingTarget in __getBindingTargets(target).iteritems():
        if bindingTarget.type == 'output':
            destination = binder.destinationForBindingTarget(name, properties)
            binding = binder.bindProducer(destination, properties)
            bindingTarget.send = binding.send

        elif bindingTarget.type == 'input':
            group = binder.groupForBindingTarget(name, properties)
            destination = binder.destinationForBindingTarget(name, properties)
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
    environment = {}
    try:
        springApplicationJson = os.environ['SPRING_APPLICATION_JSON']
        if (springApplicationJson):
            environment = json.loads(springApplicationJson)
    except:
        pass
    return environment


class cloud:
    def __init__(self, env):
        self.env = env

    def service(self, name):
        try:
            vcap_services = json.loads(self.env['VCAP_SERVICES'])
            for (serviceName, serviceInstances) in vcap_services.iteritems():
                for service in serviceInstances:
                    if (service['name'] == name):
                        return service
        except KeyError:
            raise RuntimeError('application environment does not contain \'VCAP_SERVICES\'')

    def start_health_check(self):
        def health_check():
             try:
                 PORT = int(self.env['PORT'])
             except KeyError:
                 try:
                     PORT = int(self.env['VCAP_APP_PORT'])
                 except KeyError:
                     raise RuntimeError('application environment does not contain \'PORT\' or \'VCAP_APP_PORT\'')

             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             s.bind((socket.gethostname(), PORT))
             s.listen(1)

             while 1:
                # accept connections from outside
                s.accept()

        thread = multiprocessing.Process(target=health_check)
        thread.start()
        return thread
