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

from spring.cloud.stream import components

def bind(target, binder, properties):
    for name, bindingTarget in __get_binding_targets__(target).iteritems():
        if bindingTarget.type == 'output':
            destination = binder.__destination_for_binding_target__(name, properties)
            binding = binder.bind_producer(destination, properties)
            bindingTarget.send = binding.send

        elif bindingTarget.type == 'input':
            group = binder.__group_for_binding_target__(name, properties)
            destination = binder.__destination_for_binding_target__(name, properties)
            binding = binder.bind_consumer(destination, group, properties)
            bindingTarget.receive = binding.receive

def __get_binding_targets__(object):
    bindingTargets = {}
    if object.__class__ == components.BindingTarget:
        bindingTargets[object.name] = object.type
    for (k, v) in object.__dict__.iteritems():
        if v.__class__ == components.BindingTarget:
            bindingTargets[k] = v
    return bindingTargets
