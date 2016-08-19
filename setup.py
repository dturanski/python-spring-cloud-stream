#
# Requires setuptools. From the command line, type 'pip install setuptools' if this fails.
#
from setuptools import setup, find_packages

setup(name='spring-cloud-stream',
      version = '0.1.0',
      packages = find_packages(exclude=['tests','tests.*']),
      test_suite = 'tests',
      description = 'Spring Cloud Stream for Python',
      long_description = 'Spring Cloud Stream for Python',
      url = 'https://github.com/dturanski/python-spring-cloud-stream',
      author = 'David Turanski',
      author_email = 'dturanski@pivotal.io',
      license='Apache 2.0',
      classifiers = [
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development',

            # Pick your license as you wish (should match "license" above)
            'License :: Apache 2.0 License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7'
            'Programming Language :: Python :: 3'
            'Programming Language :: Python :: 3.4'
            'Programming Language :: Python :: 3.5'
      ],
      install_requires = ['pika','kafka-python','jsonpath_rw'],
      test_requires = ['mock', 'unittest2']
      )