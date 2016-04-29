To run:

	 $export SPRING_APPLICATION_JSON="{\"spring.cloud.stream.bindings.output.producer.requiredGroups\":\"ticktock\",\"spring.cloud.stream.bindings.output.destination\":\"ticktock.time\"}"
     $./testapp.py

or 

     $./testapp.py --spring.cloud.stream.bindings.output.producer.requiredGroups=ticktock --spring.cloud.stream.bindings.output.destination=ticktock.time

