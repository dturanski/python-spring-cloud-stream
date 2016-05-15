This directory includes some simple example of Python scripts which may be deployed as a Docker image for use in a Spring Cloud Dataflow
stream.

Building the docker image
=========================

The `Dockerfile` creates a lightweight alpine container which includes python 2.7.11, pip, and setuptools Out of the box.
Currently, pip pulls the latest `spring-cloud-dataflow` module from git as specified in `requirements.txt` and installs it
in the container. In order to do this, Docker must first install git. There are many python containers available at
[](https://hub.docker.com/_/python/). The alpine one appears to have the smallest footprint. Once the dependencies are installed,
docker runs the Python script given by the `CMD` entry in the Dockerfile.

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
    these values as environment variables, but the python module also allows them to be passed as command line arguments prefixed by `--`  ,similar to Spring Boot. For example:


````
$docker run my/app src/consumer.py  --SPRING_RABBITMQ_HOST=192.168.99.100 --SPRING_RABBITMQ_PORT=32770 --spring.cloud.stream.bindings.input.group=ticktock --spring.cloud.stream.bindings.input.destination=ticktock.time
````

Here the specific group and destination values are not important but the rabbit binder requires them to bind to an exchange and queue. See specific eamples for more details.



Publishing the app to Docker Hub
================================

By default, the [Spring Cloud Mesos server](https://github.com/spring-cloud/spring-cloud-dataflow-server-mesos) pulls images from docker hub so
you will need to publish your app in order to use it in a stream. First set up a docker hub account if necessary, then login and push the app:

````
$ docker build -t <username>/<appname> .
$ docker login ...
$ docker push <username>/<appname>
````



