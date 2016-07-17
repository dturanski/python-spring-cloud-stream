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
import test_cf
import test_environment
import test_types

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(test_cf.TestCfApp))
    test_suite.addTest(unittest.makeSuite(test_environment.TestEnvironment))
    test_suite.addTest(unittest.makeSuite(test_types.TestTypes))
    return test_suite


runner=unittest.TextTestRunner()
runner.run(suite())
