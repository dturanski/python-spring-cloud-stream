import unittest
import sys
import os


sys.path.insert(0, os.path.abspath('..'))

from spring.cloud.stream.binding import BindingProperties

class TestBindingProperties(unittest.TestCase):


    properties = {
        'spring.cloud.stream.bindings.output.destination': 'ticktock.log',
        'spring.cloud.stream.bindings.output.producer.requiredGroups': 'ticktock',
        'spring.cloud.stream.bindings.output.producer.partitionKeyExpression':'foo()',
        'spring.cloud.stream.bindings.output.producer.partitionCount':3,
        'spring.cloud.stream.bindings.input.destination': 'ticktock.time',
        'spring.cloud.stream.bindings.input.group': 'ticktock',
        'spring.cloud.stream.bindings.input.consumer.partitioned': 'true',
        'spring.cloud.stream.bindings.input.consumer.headerMode': 'raw'
                  }

    def test_binding_properties_for_output(self):
        bindings = BindingProperties(TestBindingProperties.properties).binding_properties('output')
        self.assertEqual('ticktock.log',bindings['destination'])
        self.assertEqual(0, bindings['instanceIndex'])
        self.assertEqual(1, bindings['instanceCount'])
        self.assertEqual('ticktock', bindings['producer']['requiredGroups'])

    def test_binding_properties_for_input(self):
        bindings = BindingProperties(TestBindingProperties.properties).binding_properties('input')
        self.assertEqual('ticktock.time',bindings['destination'])
        self.assertEqual(0, bindings['instanceIndex'])
        self.assertEqual(1, bindings['instanceCount'])
        self.assertEqual(True, bindings['consumer']['partitioned'])
        self.assertEqual('ticktock.time', bindings['destination'])

    def test_producer_properties(self):
        producer_props = BindingProperties(TestBindingProperties.properties).producer_bindings()
        self.assertEqual('ticktock', producer_props['requiredGroups'])
        self.assertEqual('embeddedHeaders', producer_props['headerMode'])
        self.assertEqual('foo()', producer_props['partitionKeyExpression'])
        self.assertEqual(3, producer_props['partitionCount'])


    def test_consumer_properties(self):
        consumer_props = BindingProperties(TestBindingProperties.properties).consumer_bindings()
        self.assertEqual(1, consumer_props['concurrency'])
        self.assertEqual(3, consumer_props['maxAttempts'])
        self.assertEqual(1000, consumer_props['backOffInitialInterval'])
        self.assertEqual(10000, consumer_props['backOffMaxInterval'])
        self.assertEqual(2.0, consumer_props['backOffMultiplier'])
        self.assertEqual(True, consumer_props['partitioned'])
        self.assertEqual('raw', consumer_props['headerMode'])

if __name__ == '__main__':
    unittest.main()