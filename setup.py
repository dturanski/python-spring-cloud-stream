
#import ez_setup
#ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(name='spring-cloud-dataflow',
      version='0.1.0',
      packages=find_packages(),
      description = 'Spring Cloud Dataflow Binders',
      long_description = 'Spring Cloud Dataflow Binders for Python',
      url = 'https://github.com/dturanski/python-dataflow-binder',
      author='David Turanski',
      author_email='dturanski@pivotal.io',
      license='Apache 2.0',
      classifiers=[
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
      ],
      install_requires=['pika'],
      )