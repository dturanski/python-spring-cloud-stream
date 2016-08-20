import unittest
import sys
import os


sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.dirname(__file__))

from spring.cloud import environment

class TestEnvironment(unittest.TestCase):

    def tearDown(self):
        try:
            del os.environ['SPRING_APPLICATION_JSON']
            os.environ['SPRING_RABBITMQ_HOST']
        except:
            pass

    def test_env_with_args(self):
        env = environment.env(['--spring.cloud.stream.bindings.output.producer.requiredGroups=ticktock',
                               '--spring.cloud.stream.bindings.output.destination=ticktock.time'])
        self.assertEqual('ticktock', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEqual('ticktock.time', env['spring.cloud.stream.bindings.output.destination'])

    def test_default_env_is_os_env(self):
        env = environment.env(sys.argv)
        self.assertEqual(os.environ.__len__(), env.__len__())

    def test_env_from_spring_application_json(self):
        os.environ[
            'SPRING_APPLICATION_JSON'] = '{"spring.cloud.stream.bindings.output.producer.requiredGroups":"original","spring.cloud.stream.bindings.output.destination":"original.time"}'
        env = environment.env(sys.argv)
        self.assertEqual('original', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEqual('original.time', env['spring.cloud.stream.bindings.output.destination'])

    def test_env_from_os_environment(self):
        os.environ['SPRING_RABBITMQ_HOST'] = 'localhost'
        env = environment.env(sys.argv)
        self.assertEqual('localhost', env['SPRING_RABBITMQ_HOST'])

    def test_args_override_spring_application_json(self):
        os.environ[
            'SPRING_APPLICATION_JSON'] = '{"spring.cloud.stream.bindings.output.producer.requiredGroups":"original","spring.cloud.stream.bindings.output.destination":"original.time"}'
        env = environment.env(['--spring.cloud.stream.bindings.output.producer.requiredGroups=ticktock',
                               '--spring.cloud.stream.bindings.output.destination=ticktock.time'])
        self.assertEqual('ticktock', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEqual('ticktock.time', env['spring.cloud.stream.bindings.output.destination'])

    def test_include_app_config_file(self):
        env = environment.env([], configfilepath=os.path.abspath(__file__) + '/../application-test.cfg')
        self.assertEqual('group1,group2', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEqual('True', env['spring.cloud.stream.rabbit.bindings.output.producer.autoBindDlq'])
        self.assertEqual('prefix-',env['spring.cloud.stream.rabbit.bindings.output.producer.prefix'])

        self.assertEqual('5', env['spring.cloud.stream.rabbit.bindings.input.consumer.prefetch'])

    def test_env_overrides_app_config_file(self):
        os.environ[
            'SPRING_APPLICATION_JSON'] = '{"spring.cloud.stream.bindings.output.producer.requiredGroups":"override"}'
        env = environment.env([],configfilepath=os.path.abspath(__file__) + '/../application-test.cfg')
        self.assertEqual('override', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])

if __name__ == '__main__':
    unittest.main()