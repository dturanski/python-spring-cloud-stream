This is a simple example of a Python script which may be deployed as a Docker image for use in a Spring Cloud Dataflow
stream. `consumer.py` implements a simple sink which simply prints message contents to `stdout`.

See the [docker examples README](../README.md) for more details on creating and publishing the docker image.


Currently this image is published to [dturanski/consumer-app](https://hub.docker.com/r/dturanski/consumer-app/)

Creating a Stream
=================

* Set up a Mesos test cluster and start the Spring Cloud Dataflow server for Mesos, configured Rabbit MQ, transport following the instructions [here](http://docs.spring.io/spring-cloud-dataflow-server-mesos/docs/current-SNAPSHOT/reference/htmlsingle/#_deploying_streams_on_mesos_and_marathon)

* Register the required modules. We will create the traditional `ticktock` example using the standard `time` source and the python sink.
Substitute your docker image, or use mine:

````
dataflow:>module register --name time --type source --uri docker:springcloudstream/time-source-rabbit
dataflow:>module register --name consumer-app --type sink --uri docker:dturanski/consumer-app
````

* Create and deploy the stream:

````
dataflow:>stream create ticktock --definition "time | consumer-app" --deploy
````
If all goes well, you should be able to view the consumer-app output via the Mesos console [http://192.168.33.10:5050](http://192.168.33.10:5050), if using the Test cluster.
You should see an app named `ticktock-consumer-app` with a RUNNING status. Drill down on that to view `stdout`. You should see something like:

````
(" [x] Received '05/13/16 21:03:44'", <BasicProperties(['content_type=text/plain', 'delivery_mode=2', "headers={'contentType': u'text/plain'}", 'priority=0'])>)
(" [x] Received '05/13/16 21:03:45'", <BasicProperties(['content_type=text/plain', 'delivery_mode=2', "headers={'contentType': u'text/plain'}", 'priority=0'])>)
(" [x] Received '05/13/16 21:03:46'", <BasicProperties(['content_type=text/plain', 'delivery_mode=2', "headers={'contentType': u'text/plain'}", 'priority=0'])>)
(" [x] Received '05/13/16 21:03:47'", <BasicProperties(['content_type=text/plain', 'delivery_mode=2', "headers={'contentType': u'text/plain'}", 'priority=0'])>)
(" [x] Received '05/13/16 21:03:48'", <BasicProperties(['content_type=text/plain', 'delivery_mode=2', "headers={'contentType': u'text/plain'}", 'priority=0'])>)
(" [x] Received '05/13/16 21:03:49'", <BasicProperties(['content_type=text/plain', 'delivery_mode=2', "headers={'contentType': u'text/plain'}", 'priority=0'])>)
(" [x] Received '05/13/16 21:03:50'", <BasicProperties(['content_type=text/plain', 'delivery_mode=2', "headers={'contentType': u'text/plain'}", 'priority=0'])>)
(" [x] Received '05/13/16 21:03:51'", <BasicProperties(['content_type=text/plain', 'delivery_mode=2', "headers={'contentType': u'text/plain'}", 'priority=0'])>)
(" [x] Received '05/13/16 21:03:52'", <BasicProperties(['content_type=text/plain', 'delivery_mode=2', "headers={'contentType': u'text/plain'}", 'priority=0'])>)
(" [x] Received '05/13/16 21:03:53'", <BasicProperties(['content_type=text/plain', 'delivery_mode=2', "headers={'contentType': u'text/plain'}", 'priority=0'])>)
(" [x] Received '05/13/16 21:03:54'", <BasicProperties(['content_type=text/plain', 'delivery_mode=2', "headers={'contentType': u'text/plain'}", 'priority=0'])>)
````





