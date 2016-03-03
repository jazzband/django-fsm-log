#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-fsm-log',
    version='1.3.0',
    description='Logging for django-fsm',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/django-fsm-log',
    packages=find_packages(),
    install_requires=['django>=1.6', 'django_fsm>=2', 'django_appconf']
)
