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
import configparser
import logging

logger = logging.getLogger(__name__)

def env(args, sources=['./application.cfg']):
    environment = {}
    if (not isinstance(sources, list)):
        sources = [sources]

    for source in sources:
        config = None
        if (isinstance(source,str)):
            config = __read_config_file__(source)
        elif (isinstance(source, configparser.ConfigParser)):
            config = source
        if (config):
            environment.update(__merge_config__(config))

    environment.update(os.environ)
    environment.update(__parse_spring_application_json__())
    environment.update(__parse_command_line__(args))
    return environment

def __parse_command_line__(args):
    environment = {}
    if (args):
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
    config = None
    filepath = os.path.abspath(str(filepath))
    if (os.path.exists(filepath)):
        logger.info('reading config file [' + filepath + ']')
        open(filepath)
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(filepath)
    return config

def __merge_config__(config):
    """Parse python config file and convert to properties"""
    environment = {}
    for section in config.sections():
        for item in config.items(section):
            key = section + '.' + item[0]
            environment[key] = item[1]
    return environment






