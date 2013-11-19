#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-fsm-log',
    version='0.2',
    description='Logging for django-fsm',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/django_fsm_log',
    packages=find_packages(),
    install_requires=['django', 'south', 'django_fsm']
)
