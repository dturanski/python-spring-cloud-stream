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
import ConfigParser
import logging

logger = logging.getLogger(__name__)

def env(args, configfilepath='./application.cfg'):
    environment = __read_config_file__(configfilepath)
    environment.update(os.environ)
    environment.update(__parse_spring_application_json__())
    environment.update(__parse_command_line__(args))
    return environment

def __parse_command_line__(args):
    environment = {}
    if (args and len(args) > 0):
        for arg in args:
            if (arg.startswith('--')):
                try:
                    (key, value) = arg.split("=")
                    key = key.replace('--', '')
                    environment[key] = value
                except:
                    logger.warn('cannot not parse command line argument ' + arg)
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

def __read_config_file__(filepath):
    """Parse python config file and convert to properties"""
    filepath = os.path.abspath(filepath)
    logger.info('reading config file [' + filepath + ']' + ' file exists: ' + str(os.path.exists(filepath)))
    environment = {}
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read(filepath)
    for section in config.sections():
        for item in config.items(section):
            key = section + '.' + item[0]
            environment[key] = item[1]
    return environment






