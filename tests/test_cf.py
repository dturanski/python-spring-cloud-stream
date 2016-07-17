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
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath('..'))

from spring.cloud.cf import App

class TestCfApp(unittest.TestCase):

    def test_service(self):
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

        rabbit = App(env).service('rabbit')
        self.assertEquals('rabbit', rabbit['name'])
        self.assertEquals('amqp://xgkwomgl:aIUHpX761b_pnC9tLnbaVOZAyE9s_1mH@fox.rmq.cloudamqp.com/xgkwomgl',
                          rabbit['credentials']['uri'])

if __name__ == '__main__':
    unittest.main()