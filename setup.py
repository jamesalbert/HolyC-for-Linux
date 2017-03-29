#!/usr/bin/env python

from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session='holyc')
reqs = [str(ir.req) for ir in install_reqs]

setup(name='secularize',
      version='0.0.1',
      description='run HolyC source on linux...and secularify wasn\'t as catchy',
      author='James Albert',
      author_email='jalbert1@uci.edu',
      url='https://www.github.com/jamesalbert/HolyC-for-Linux',
      install_requires=reqs,
      packages=['secularize'],
     )
