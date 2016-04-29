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
