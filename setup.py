#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-fsm-log',
    version='1.5.0',
    description='Logging for django-fsm',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/django-fsm-log',
    license='MIT',
    packages=find_packages(),
    install_requires=['django>=1.8', 'django_fsm>=2', 'django_appconf'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
