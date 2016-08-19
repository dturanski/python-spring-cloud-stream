import unittest
import sys
import os


sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.dirname(__file__))

from spring.cloud import environment
from spring.cloud.stream.binder.rabbit import Binder
from spring.cloud.stream.binding import BindingProperties
from spring.cloud.stream.components import Sink,Source,Processor
import unittest2 as unittest
import mock
from mock import MagicMock
import pika


class TestBinder(unittest.TestCase):

    def setUp(self):
        pika.BlockingConnection.__init__ = mock.MagicMock(return_value=None)
        self.connection = pika.BlockingConnection(pika.URLParameters('amqp://somehost:5672'))
        self.channel = mock.MagicMock(return_value=None)
        pika.channel.Channel.exchange_declare = self.channel
        pika.BlockingConnection.channel = mock.MagicMock(return_value=self.channel)
        self.binder = Binder(self.connection,
                    env=environment.env([], configfilepath=os.path.abspath(__file__) + '/../application-test.cfg'))

    def test_bind_producer(self):
        producer = Source()
        producer.bind(self.binder)
        self.channel.exchange_declare.assert_called_with(exchange='prefix-destination', type='topic', durable=True)
        self.channel.queue_declare.assert_any_call(queue ='prefix-destination.group1', durable=True)
        self.channel.queue_declare.assert_any_call(queue ='prefix-destination.group2', durable=True)

        self.channel.queue_bind.assert_any_call(exchange ='prefix-destination', queue='prefix-destination.group1',
                                              routing_key='destination')
        self.channel.queue_bind.assert_any_call(exchange='prefix-destination', queue='prefix-destination.group2',
                                              routing_key ='destination')

    def test_bind_consumer(self):
        consumer = Sink()
        consumer.bind(self.binder)
        self.channel.exchange_declare.assert_called_with(exchange='destination_out', type='topic', durable=True)
        self.channel.queue_declare.assert_called_with(queue ='destination_out.group1', durable=True)
        self.channel.queue_bind.assert_called_with(exchange ='destination_out', queue='destination_out.group1',
                                             routing_key='#')

if __name__ == '__main__':
    unittest.main()