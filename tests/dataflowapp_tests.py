import unittest
import sys
import os
import json
from spring.cloud.dataflow import dataflowapp


class TestDatalowApp(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, os.path.abspath('..'))

    def test_env_with_args(self):
        del os.environ['SPRING_APPLICATION_JSON']
        env = dataflowapp.env(['--spring.cloud.stream.bindings.output.producer.requiredGroups=ticktock',
                               '--spring.cloud.stream.bindings.output.destination=ticktock.time'])
        self.assertEquals('ticktock', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEquals('ticktock.time', env['spring.cloud.stream.bindings.output.destination'])

    def test_default_env_is_os_env(self):
        del os.environ['SPRING_APPLICATION_JSON']
        env = dataflowapp.env(sys.argv)
        self.assertEquals(os.environ.__len__(), env.__len__())

    def test_env_from_spring_application_json(self):
        os.environ[
            'SPRING_APPLICATION_JSON'] = '{"spring.cloud.stream.bindings.output.producer.requiredGroups":"original","spring.cloud.stream.bindings.output.destination":"original.time"}'
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
        env = dataflowapp.env(['--spring.cloud.stream.bindings.output.producer.requiredGroups=ticktock',
                               '--spring.cloud.stream.bindings.output.destination=ticktock.time'])
        self.assertEquals('ticktock', env['spring.cloud.stream.bindings.output.producer.requiredGroups'])
        self.assertEquals('ticktock.time', env['spring.cloud.stream.bindings.output.destination'])

    def test_cloud(self):
        env = {}

        env['VCAP_SERVICES'] = '''
        {
    "cloudamqp": [
        {
            "credentials": {
                "http_api_uri": "https://xgkwomgl:aIUHpX761b_pnC9tLnbaVOZAyE9s_1mH@fox.rmq.cloudamqp.com/api/",
                "uri": "amqp://xgkwomgl:aIUHpX761b_pnC9tLnbaVOZAyE9s_1mH@fox.rmq.cloudamqp.com/xgkwomgl"
            },
            "label": "cloudamqp",
            "name": "rabbit",
            "plan": "lemur",
            "provider": null,
            "syslog_drain_url": null,
            "tags": [
                "Web-based",
                "User Provisioning",
                "Messaging and Queuing",
                "amqp",
                "Backup",
                "Single Sign-On",
                "New Product",
                "rabbitmq",
                "Certified Applications",
                "Android",
                "Developer Tools",
                "Development and Test Tools",
                "Buyable",
                "Messaging",
                "Importable",
                "IT Management"
            ]
        }
    ],
    "rediscloud": [
        {
            "credentials": {
                "hostname": "pub-redis-19134.us-east-1-4.3.ec2.garantiadata.com",
                "password": "uqb00vw2XIZu91Yk",
                "port": "19134"
            },
            "label": "rediscloud",
            "name": "redis",
            "plan": "30mb",
            "provider": null,
            "syslog_drain_url": null,
            "tags": [
                "Data Stores",
                "Data Store",
                "Caching",
                "Messaging and Queuing",
                "key-value",
                "caching",
                "redis"
            ]
        }
    ]
}
        '''

        rabbit = dataflowapp.cloud(env).service('rabbit')
        self.assertEquals('rabbit', rabbit['name'])
        self.assertEquals('amqp://xgkwomgl:aIUHpX761b_pnC9tLnbaVOZAyE9s_1mH@fox.rmq.cloudamqp.com/xgkwomgl',
                          rabbit['credentials']['uri'])
