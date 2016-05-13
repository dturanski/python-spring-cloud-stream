NOTE: Currently does not support Python 3

This includes example apps `producer.py` and `consumer.py` that you can run standalone. To run them as is, first start a rabbitmq-server on localhost.

To send a message:

	 $export SPRING_APPLICATION_JSON="{\"spring.cloud.stream.bindings.output.producer.requiredGroups\":\"ticktock\",\"spring.cloud.stream.bindings.output.destination\":\"ticktock.time\"}"
     $./producer.py

or 

     $./producer.py --spring.cloud.stream.bindings.output.producer.requiredGroups=ticktock --spring.cloud.stream.bindings.output.destination=ticktock.time

This will send a single message each time it is run.

To receive messages:

    $export SPRING_APPLICATION_JSON="{\"spring.cloud.stream.bindings.input.group\":\"ticktock\",\"spring.cloud.stream.bindings.input.destination\":\"ticktock.time\"}"
     $./consumer.py

or

     $./consumer.py --spring.cloud.stream.bindings.input.group=ticktock --spring.cloud.stream.bindings.input.destination=ticktock.time
