import unittest
import sys
import os


sys.path.insert(0, os.path.abspath('..'))
from spring.cloud import environment


class TestEnvironment(unittest.TestCase):

    def test_env_with_args(self):
        del os.environ['SPRING_APPLICATION_JSON']
        env = environment.env(['--spring.cloud.stream.bindings.output.producer.requiredGroups=ticktock',
                               '--spring.cloud.stream.bindings.output.destination=ticktock.time'])
        self.assertEquals('ticktock', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEquals('ticktock.time', env['spring.cloud.stream.bindings.output.destination'])

        output_props = environment.config_props(env,'spring.cloud.stream.bindings.output')
        self.assertEquals('ticktock',output_props['producer.requiredGroups'])
        self.assertEquals('ticktock.time',output_props['destination'])



    def test_default_env_is_os_env(self):
        del os.environ['SPRING_APPLICATION_JSON']
        env = environment.env(sys.argv)
        self.assertEquals(os.environ.__len__(), env.__len__())

    def test_env_from_spring_application_json(self):
        os.environ[
            'SPRING_APPLICATION_JSON'] = '{"spring.cloud.stream.bindings.output.producer.requiredGroups":"original","spring.cloud.stream.bindings.output.destination":"original.time"}'
        env = environment.env(sys.argv)
        self.assertEquals('original', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEquals('original.time', env['spring.cloud.stream.bindings.output.destination'])

    def test_env_from_os_environment(self):
        os.environ['SPRING_RABBITMQ_HOST'] = 'localhost'
        env = environment.env(sys.argv)
        self.assertEquals('localhost', env['SPRING_RABBITMQ_HOST'])

    def test_args_override_spring_application_json(self):
        os.environ[
            'SPRING_APPLICATION_JSON'] = '{"spring.cloud.stream.bindings.output.producer.requiredGroups":"original","spring.cloud.stream.bindings.output.destination":"original.time"}'
        env = environment.env(sys.argv)
        env = environment.env(['--spring.cloud.stream.bindings.output.producer.requiredGroups=ticktock',
                               '--spring.cloud.stream.bindings.output.destination=ticktock.time'])
        self.assertEquals('ticktock', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEquals('ticktock.time', env['spring.cloud.stream.bindings.output.destination'])

if __name__ == '__main__':
    unittest.main()