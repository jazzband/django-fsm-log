#!/usr/bin/env python

from distutils.core import setup

setup(
    name='django-fsm-log',
    version='0.1',
    description='Logging for django-fsm',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/django_fsm_log',
    packages=['django_fsm_log'],
    install_requires=['django', 'south', 'django_fsm']
)
