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

To install the Spring Cloud Dataflow binder modules:

     $sudo python ./setup.py install