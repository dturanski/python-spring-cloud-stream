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

def env(args):
    environment = os.environ
    environment.update(__parse_spring_application_json__())

    for arg in args:
        if (arg.startswith('--')):
            (key, value) = arg.split("=")
            key = key.replace('--', '')
            environment[key] = value
    return environment

def __parse_spring_application_json__():
    environment = {}
    try:
        springApplicationJson = os.environ['SPRING_APPLICATION_JSON']
        if (springApplicationJson):
            environment = json.loads(springApplicationJson)
    except:
        pass
    return environment
