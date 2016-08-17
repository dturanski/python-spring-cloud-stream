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
class BindingTarget:
    def __init__(self,name):
        self.name = name


class Source(BindingTarget):
    def __init__(self):
        BindingTarget.__init__(self,'output')

    def bind(self, binder, properties):
        #TODO - Do not use private method here
        destination = binder.__destination_for_binding_target__(self.name, properties)
        binder.bind_producer(destination, self, properties)


class Sink(BindingTarget):
    def __init__(self):
        BindingTarget.__init__(self, 'input')

    def bind(self, binder, properties):
        # TODO - Do not use private methods here
        group = binder.__group_for_binding_target__(self.name, properties)
        destination = binder.__destination_for_binding_target__(self.name, properties)
        binder.bind_consumer(destination, group, self, properties)

class Processor(Source, Sink):
    def __init__(self):
        self.input = Sink()
        self.output = Source()

    def bind(self, binder, properties):
        self.input.bind(binder,properties)
        self.output.bind(binder,properties)

    def send(self, message):
        self.output.send(message)

    def receive(self, callback):
        return self.input.receive(callback);

