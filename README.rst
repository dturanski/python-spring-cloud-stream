Python Spring Cloud Stream
==========================

This is a Python implementation of Spring Cloud Stream to support
deploying native Python scripts as Spring Cloud Stream 
applications. Please review the 
`examples <https://github.com/dturanski/python-spring-cloud-stream/tree/master/examples>`_ 
directory for details on how to use this module.

This module provides compatibility with Spring Cloud Stream bindings 
used to auto-configure messaging transport using the same 
`spring.cloud.stream.*` properties. The
programming model does not use Spring so things like Spring DI, 
Annotations and `MessageChannel`, and SpEL are not supported. But the
aim is that transport configuration emulates Spring Cloud
Stream apps written in Java with Spring.

Properties can be passed as environment variables, command line args,
or Python config file(default ./application.cfg). The order of
precedence is command line args, environment variables, and config
file.

To install the Spring Cloud Stream module:

* You may need to install pip
* You may need to change permissions or run the following as sudo


| `$pip install setuptools`
| `$python ./setup.py install`

