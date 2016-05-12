import unittest
import sys
import os
from spring.cloud.dataflow import dataflowapp
class TestDatalowApp(unittest.TestCase):
    def test_env_with_args(self):
        del os.environ['SPRING_APPLICATION_JSON']
        env = dataflowapp.env(['--spring.cloud.stream.bindings.output.producer.requiredGroups=ticktock','--spring.cloud.stream.bindings.output.destination=ticktock.time'])
        self.assertEquals('ticktock', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEquals('ticktock.time', env['spring.cloud.stream.bindings.output.destination'])

    def test_default_env_is_os_env(self):
        del os.environ['SPRING_APPLICATION_JSON']
        env = dataflowapp.env(sys.argv)
        self.assertEquals(os.environ.__len__(),env.__len__())

    def test_env_from_spring_application_json(self):
        os.environ[ 'SPRING_APPLICATION_JSON'] = '{"spring.cloud.stream.bindings.output.producer.requiredGroups":"original","spring.cloud.stream.bindings.output.destination":"original.time"}'
        env = dataflowapp.env(sys.argv)
        self.assertEquals('original', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEquals('original.time', env['spring.cloud.stream.bindings.output.destination'])

    def test_env_from_os_environment(self):
        os.environ['SPRING_RABBITMQ_HOST'] = 'localhost'
        env = dataflowapp.env(sys.argv)
        self.assertEquals('localhost', env['SPRING_RABBITMQ_HOST'])

    def test_args_override_spring_application_json(self):
        os.environ[
            'SPRING_APPLICATION_JSON'] = '{"spring.cloud.stream.bindings.output.producer.requiredGroups":"original","spring.cloud.stream.bindings.output.destination":"original.time"}'
        env = dataflowapp.env(sys.argv)
        env = dataflowapp.env(['--spring.cloud.stream.bindings.output.producer.requiredGroups=ticktock','--spring.cloud.stream.bindings.output.destination=ticktock.time'])
        self.assertEquals('ticktock', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEquals('ticktock.time', env['spring.cloud.stream.bindings.output.destination'])
