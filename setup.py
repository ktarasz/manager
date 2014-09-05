from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='manager',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'Flask==0.10.1',
            'Flask-SocketIO',
            'Jinja2==2.7.2',
            'MarkupSafe==0.18',
            'Werkzeug==0.9.4',
            'gevent==1.0',
            'gevent-socketio==0.3.6',
            'gevent-websocket==0.9.2',
            'greenlet==0.4.2',
            'itsdangerous==0.23',
            'ujson==1.33',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
