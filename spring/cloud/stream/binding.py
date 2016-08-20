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

class BindingProperties:
    PREFIX = 'spring.cloud.stream'
    BINDINGS_PREFIX = PREFIX + '.bindings'

    def __init__(self,properties):
        self.properties=properties
        stream_props = config_props(self.properties, BindingProperties.PREFIX)

        self.instance_count = int(stream_props.get('instanceCount', 1))


        self.instance_index = int(stream_props.get('instanceIndex',-1))
        self.instance_index = int(
            properties.get('INSTANCE_INDEX', -1)) if self.instance_index < 0  else self.instance_index
        self.instance_index = int(
            properties.get('CF_INSTANCE_INDEX', -1)) if self.instance_index < 0  else self.instance_index
        self.instance_index = 0 if self.instance_index < 0 else self.instance_index


    def binding_properties(self, channel_name):
        bindings = config_props(self.properties, BindingProperties.BINDINGS_PREFIX + '.' + channel_name)
        bindings['producer'] = self.producer_bindings(channel_name)
        bindings['consumer'] = self.consumer_bindings(channel_name)
        bindings['instanceIndex'] = self.instance_index
        bindings['instanceCount'] = self.instance_count
        return bindings

    def producer_bindings(self, producer_name='output'):
        producer_bindings = config_props(self.properties, BindingProperties.BINDINGS_PREFIX + '.' + producer_name + '.' + 'producer')
        producer_bindings['partitionCount'] = int(producer_bindings.get('partitionCount', 1))
        producer_bindings['headerMode'] = producer_bindings.get('headerMode', 'embeddedHeaders')
        producer_bindings['name'] = producer_name
        return producer_bindings

    def consumer_bindings(self, consumer_name='input'):
        consumer_bindings = config_props(self.properties, BindingProperties.BINDINGS_PREFIX + '.' + consumer_name + '.' + 'consumer')
        consumer_bindings['concurrency'] = int(consumer_bindings.get('concurrency', 1))
        consumer_bindings['maxAttempts'] = int(consumer_bindings.get('maxAttempts', 3))
        consumer_bindings['backOffInitialInterval'] = int(consumer_bindings.get('backOffInitialInterval', 1000))
        consumer_bindings['backOffMaxInterval'] = int(consumer_bindings.get('backOffMaxInterval', 10000))
        consumer_bindings['backOffMultiplier'] = float(consumer_bindings.get('backOffMultiplier', 2.0))
        consumer_bindings['partitioned'] = bool(consumer_bindings.get('partitioned',False))
        consumer_bindings['name'] = consumer_name
        return consumer_bindings


def config_props(properties, prefix):
    props = {}
    pre = prefix + '.'
    for key, value in properties.items():
        if (key.startswith(pre)):
            suffix = key[len(pre):]
            # don't include compound names (e.g., producer.foo)
            if (suffix.find('.') == -1):
                props[suffix] = value
    return props

class RabbitBindingProperties:
    PREFIX = 'spring.cloud.stream.rabbit.bindings'

    def __init__(self, properties):
       self.properties = properties

    def producer_bindings(self, producer_name='output'):
        producer_bindings = config_props(self.properties, RabbitBindingProperties.PREFIX + '.' + producer_name + '.' + 'producer')
        producer_bindings['autoBindDlq'] = bool(producer_bindings.get('autoBindDlq' ,False))
        producer_bindings['batchingEnabled'] = bool(producer_bindings.get('batchingEnabled', False))
        producer_bindings['batchSize'] = int(producer_bindings.get('batchingEnabled', 100))
        producer_bindings['batchBufferLimit'] = int(producer_bindings.get('batchBufferLimit', 10000))
        producer_bindings['batchTimeout'] = int(producer_bindings.get('batchTimeout', 5000))
        producer_bindings['compress'] = bool(producer_bindings.get('compress', False))
        producer_bindings['deliveryMode'] = producer_bindings.get('deliveryMode', 'PERSISTENT')
        producer_bindings['prefix'] = producer_bindings.get('prefix', '')
        producer_bindings['requestHeaderPatterns'] = producer_bindings.get('requestHeaderPatterns',
                                                                           '[STANDARD_REQUEST_HEADERS, \'*\']')
        producer_bindings['replyHeaderPatterns'] = producer_bindings.get('replyHeaderPatterns',
                                                                           '[STANDARD_REPLY_HEADERS, \'* \']')
        producer_bindings['name'] = producer_name
        return producer_bindings

    def consumer_bindings(self, consumer_name='input'):
        consumer_bindings = config_props(self.properties, RabbitBindingProperties.PREFIX + '.' + consumer_name + '.' + 'consumer')
        consumer_bindings['acknowledgeMode'] = consumer_bindings.get('acknowledgeMode', 'AUTO')
        consumer_bindings['autoBindDlq'] = bool(consumer_bindings.get('autoBindDlq', False))
        #only effective if 'group' has been set
        consumer_bindings['durableSubscription'] = bool(consumer_bindings.get('durableSubscription', True))
        consumer_bindings['maxConcurrency'] = int(consumer_bindings.get('maxConcurrency', 1))
        consumer_bindings['prefetch'] = int(consumer_bindings.get('prefetch', 1))
        consumer_bindings['prefix'] = consumer_bindings.get('prefix', '')
        consumer_bindings['recoveryInterval'] = int(consumer_bindings.get('recoveryInterval', 5000))
        consumer_bindings['requeueRejected'] = bool(consumer_bindings.get('requeueRejected', False))
        consumer_bindings['requestHeaderPatterns'] = consumer_bindings.get('requestHeaderPatterns',
                                                                           '[STANDARD_REQUEST_HEADERS,' * ']')
        consumer_bindings['replyHeaderPatterns'] = consumer_bindings.get('replyHeaderPatterns',
                                                                         '[STANDARD_REPLY_HEADERS,' * ']')
        consumer_bindings['republishToDlq'] = bool(consumer_bindings.get('republishToDlq', False))
        consumer_bindings['transacted'] = bool(consumer_bindings.get('transacted', False))
        consumer_bindings['txSize'] = int(consumer_bindings.get('txSize', 1))
        consumer_bindings['name'] = consumer_name
        return consumer_bindings
