This is a simple example of a Python script which may be deployed as a Docker image for use in a Spring Cloud Dataflow
stream. `consumer.py` implements a simple sink which simply prints message contents to `stdout`.

Building the docker image
=========================

The `Dockerfile` creates a lightweight alpine container which includes python 2.7.11, pip, and setuptools Out of the box.
Currently, pip pulls the latest `spring-cloud-dataflow` module from git as specified in `requirements.txt` and installs it
in the container. In order to do this, Docker must first install git. There are many python containers available at
[](https://hub.docker.com/_/python/). The alpine one appears to have the smallest footprint. Once the dependencies are installed,
docker runs `consumer.py`.

To build the image:

      $ docker build -t <namespace>/<image> .

If you run it locally

      $ docker run my/app

You should get the following error:

````
Traceback (most recent call last):
  File "src/consumer.py", line 10, in <module>
    connectionUrl = 'amqp://{0}:{1}'.format(env['SPRING_RABBITMQ_HOST'],env['SPRING_RABBITMQ_PORT'])
  File "/usr/local/lib/python2.7/UserDict.py", line 40, in __getitem__
    raise KeyError(key)
KeyError: 'SPRING_RABBITMQ_HOST'
````
This is a good thing because it means python and the imported modules were installed correctly.

To test it, you need to start a Rabbit MQ broker to which this app can connect. The following steps work on a Mac.

* Run a rabbit MQ docker image with management console enabled:

````
$ docker run -P -d --hostname my-rabbit --name some-rabbit rabbitmq:3-management
````

* Determine the host and mapped port of the broker

````
$ docker ps

CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS                                                                                                  NAMES
a5def64bbe38        rabbitmq:3-management   "/docker-entrypoint.s"   About an hour ago   Up About an hour    0.0.0.0:32771->4369/tcp, 0.0.0.0:32770->5672/tcp, 0.0.0.0:32769->15672/tcp, 0.0.0.0:32768->25672/tcp   some-rabbit
````

* Note the port mappings `0.0.0.0:32770->5672/tcp` and `0.0.0.0:32769->15672/tcp` .The `0.0.0.0` refers to the docker host. To determine
   it's IP Address:

````
$ docker-machine ls

NAME      ACTIVE   DRIVER       STATE     URL                         SWARM
default   *        virtualbox   Running   tcp://192.168.99.100:2376
````

In this case there is only the `default` machine on `192.168.99.100`

* Run the app providing required properties. The [Spring Cloud Dataflow Mesos server](https://github.com/spring-cloud/spring-cloud-dataflow-server-mesos) automatically sets
    these values as environment variables, but the python module also allows them to be passed as command line arguments prefixed by `--`  ,similar to Spring Boot:


````
$docker run my/app src/consumer.py  --SPRING_RABBITMQ_HOST=192.168.99.100 --SPRING_RABBITMQ_PORT=32770 --spring.cloud.stream.bindings.input.group=ticktock --spring.cloud.stream.bindings.input.destination=ticktock.time
````

Here the specific group and destination values are not important but the rabbit binder requires them to bind to an exchange and queue.

* If all is well, this will wait for messages on the queue. Publish some messages via the Rabbit MQ admin console, using the docker host
IP and mapped port. In this case [](http://192.168.99.100:32769). Navigate to the queue `ticktock.time.ticktock` and publish a message.
You should see something like

````
(" [x] Received 'Hello'", <BasicProperties(['delivery_mode=1', 'headers={}'])>)
````
 In the console where the app is running.

Publishing the app to Docker Hub
================================

By default, the [Spring Cloud Mesos server](https://github.com/spring-cloud/spring-cloud-dataflow-server-mesos) pulls images from docker hub so
you will need to publish your app in order to use it in a stream. First set up a docker hub account if necessary, then login and push the app:

````
$ docker build -t <username>/<appname> .
$ docker login ...
$ docker push <username>/<appname>
````

Currently this image is published to [dturanski/consumer-app](https://hub.docker.com/r/dturanski/consumer-app/)

Creating a Stream
=================

* Set up a Mesos test cluster and start the Spring Cloud Dataflow server for Mesos, configured Rabbit MQ, transport following the instructions [here](http://docs.spring.io/spring-cloud-dataflow-server-mesos/docs/current-SNAPSHOT/reference/htmlsingle/#_deploying_streams_on_mesos_and_marathon)

* Register the required modules. We will create the traditional `ticktock` example using the standard `time` source and the python sink.
Substitute your docker image, or use mine:

````
dataflow:>module register --name time --type source --uri docker:springcloudstream/time-source-rabbit
dataflow:>module register --name consumer-app --type sink --uri docker:dturanski/consumer-app:v0.0.1
````

* Create and deploy the stream:

````
dataflow:>stream create ticktock --definition "time | consumer-app" --deploy
````
If all goes well, you should be able to view the consumer-app output via the Mesos console [](http://192.168.33.10:5050), if using the Test cluster.
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





