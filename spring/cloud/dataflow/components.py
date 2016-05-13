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
    def __init__(self,name,type):
        self.name = name
        self.type = type
    def send(self):
        pass
    def receive(self):
        pass

class Source:
    def __init__(self):
        self.output = BindingTarget('output','output')

    def send(self, message):
        return self.output.send(message)

class Sink:
    def __init__(self):
        self.input =  BindingTarget('input','input')

    def receive(self, callback):
        return self.input.receive(callback)

#TODO: clean up inheritance
class Processor(Source, Sink):
    def __init__(self):
        self.input = BindingTarget('input','input')
        self.output = BindingTarget('output','output')
