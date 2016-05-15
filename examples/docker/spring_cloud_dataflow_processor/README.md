This is a simple example of a Python script which may be deployed as a Docker image for use in a Spring Cloud Dataflow
stream. `processor.py` implements a simple processor which performs a simple transformation converting plain text to json including
the original payload and the reversed payload.

See the [docker examples README](../README.md) for more details on creating and publishing the docker image.

Currently this image is published to [dturanski/processor](https://hub.docker.com/r/dturanski/processor/)

Creating a Stream
=================

* Set up a Mesos test cluster and start the Spring Cloud Dataflow server for Mesos, configured Rabbit MQ, transport following the instructions [here](http://docs.spring.io/spring-cloud-dataflow-server-mesos/docs/current-SNAPSHOT/reference/htmlsingle/#_deploying_streams_on_mesos_and_marathon)

* Register the required modules. We will create the traditional `ticktock` example using the standard `time` source and the python sink.
Substitute your docker image, or use mine:

````
dataflow:>module register --name time --type source --uri docker:springcloudstream/time-source-rabbit
dataflow:>module register --name log --type sink --uri docker:springcloudstream/log-sink-rabbit
dataflow:>module register --name my-processor --type processor --uri docker:dturanski/processor
````

* Create and deploy the stream:

````
dataflow:>stream create ticktock2 --definition "time | my-processor | log --inputType=text/plain" --deploy
````
If all goes well, you should be able to view the log output via the Mesos console [http://192.168.33.10:5050](http://192.168.33.10:5050), if using the Test cluster.
You should see an app named `ticktock2-log` with a RUNNING status. Drill down on that to view `stdout`. You should see something like:


````
2016-05-15 12:39:31.010  INFO 1 --- [ocessor.test3-1] log.sink                                 : {"reversed": "13:93:21 61/51/50", "original": "05/15/16 12:39:31"}
2016-05-15 12:39:32.014  INFO 1 --- [ocessor.test3-1] log.sink                                 : {"reversed": "23:93:21 61/51/50", "original": "05/15/16 12:39:32"}
2016-05-15 12:39:33.013  INFO 1 --- [ocessor.test3-1] log.sink                                 : {"reversed": "33:93:21 61/51/50", "original": "05/15/16 12:39:33"}
2016-05-15 12:39:34.023  INFO 1 --- [ocessor.test3-1] log.sink                                 : {"reversed": "43:93:21 61/51/50", "original": "05/15/16 12:39:34"}
2016-05-15 12:39:35.027  INFO 1 --- [ocessor.test3-1] log.sink                                 : {"reversed": "53:93:21 61/51/50", "original": "05/15/16 12:39:35"}
2016-05-15 12:39:36.028  INFO 1 --- [ocessor.test3-1] log.sink                                 : {"reversed": "63:93:21 61/51/50", "original": "05/15/16 12:39:36"}
2016-05-15 12:39:37.029  INFO 1 --- [ocessor.test3-1] log.sink                                 : {"reversed": "73:93:21 61/51/50", "original": "05/15/16 12:39:37"}
2016-05-15 12:39:38.032  INFO 1 --- [ocessor.test3-1] log.sink                                 : {"reversed": "83:93:21 61/51/50", "original": "05/15/16 12:39:38"}
2016-05-15 12:39:39.036  INFO 1 --- [ocessor.test3-1] log.sink                                 : {"reversed": "93:93:21 61/51/50", "original": "05/15/16 12:39:39"}
2016-05-15 12:39:40.039  INFO 1 --- [ocessor.test3-1] log.sink                                 : {"reversed": "04:93:21 61/51/50", "original": "05/15/16 12:39:40"}
2016-05-15 12:39:41.042  INFO 1 --- [ocessor.test3-1] log.sink                                 : {"reversed": "14:93:21 61/51/50", "original": "05/15/16 12:39:41"}
20
````

Alternately you can use the Python sink from the sister example:

````
dataflow:>module register --name consumer-app --type sink --uri docker:dturanski/consumer-app
````

````
dataflow:>stream create ticktock2 --definition "time | my-processor | consumer-app" --deploy
````
Note, the `--inputType` conversion is not required in this case. If all goes well, you should be able to view the consumer-app output via the Mesos console [http://192.168.33.10:5050](http://192.168.33.10:5050), if using the Test cluster.
You should see an app named `ticktock2-consumer-app` with a RUNNING status. Drill down on that to view `stdout`. You should see something like:

````
(' [x] Received \'{"reversed": "25:40:21 61/51/50", "original": "05/15/16 12:04:52"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "35:40:21 61/51/50", "original": "05/15/16 12:04:53"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "45:40:21 61/51/50", "original": "05/15/16 12:04:54"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "55:40:21 61/51/50", "original": "05/15/16 12:04:55"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "65:40:21 61/51/50", "original": "05/15/16 12:04:56"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "75:40:21 61/51/50", "original": "05/15/16 12:04:57"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "85:40:21 61/51/50", "original": "05/15/16 12:04:58"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "95:40:21 61/51/50", "original": "05/15/16 12:04:59"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "00:50:21 61/51/50", "original": "05/15/16 12:05:00"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "10:50:21 61/51/50", "original": "05/15/16 12:05:01"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "20:50:21 61/51/50", "original": "05/15/16 12:05:02"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "30:50:21 61/51/50", "original": "05/15/16 12:05:03"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "40:50:21 61/51/50", "original": "05/15/16 12:05:04"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "50:50:21 61/51/50", "original": "05/15/16 12:05:05"}\'', <BasicProperties>)
(' [x] Received \'{"reversed": "60:50:21 61/51/50", "original": "05/15/16 12:05:06"}\'', <BasicProperties>)
````





