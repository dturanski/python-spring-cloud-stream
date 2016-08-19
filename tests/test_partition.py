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

import unittest
import sys
import os

from jsonpath_rw import parse
import json

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.dirname(__file__))

class TestPartition(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPartition, self).__init__(*args, **kwargs)
        self.body = '{"id":"abcde","data":{"val1":"123","val2":"abc"}}'
        self.properties  = {
            'a': 'value',
            'another': 'value',
            'bar' : 'hello'
        }
    '''
    Test simple mechanism for invoking a function by name. E.g.,
    --partitionSelector='foo.bar'
    '''
    def test_simple(self):
        _selector = __import__('foo')
        func = getattr(_selector, 'bar')

        body = '{"id":"abcde"}'
        self.assertEquals('abcde-hello',func(self.body,self.properties))

    def test_nested_module(self):
        selector_function_ref = "nested.deep.module.bar"

        index = selector_function_ref.rfind(".")

        _module = selector_function_ref[index+1:]
        _package = selector_function_ref[:index]
        _selector = __import__(_package, globals(), locals(), [_module])

        func = getattr(_selector, _module)
        self.assertEquals('123-value', func(self.body, self.properties))

    def test_jsonpath(self):
        val = json.loads(self.body)
        data = [match.value.encode('UTF-8') for match in parse('*.val2').find(val)]
        print(data)
