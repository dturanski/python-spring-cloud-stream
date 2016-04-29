To run:

	$export SPRING_APPLICATION_JSON="{\"spring.cloud.stream.bindings.output.producer.requiredGroups\":\"ticktock\",\"spring.cloud.stream.bindings.output.destination\":\"ticktock.time\"}"
    $python spring-cloud-dataflow/binder.py

or 
	python spring-cloud-dataflow/binder.py --spring.cloud.stream.bindings.output.producer.requiredGroups=ticktock --spring.cloud.stream.bindings.output.destination=ticktock.time
