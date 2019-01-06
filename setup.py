#!/usr/bin/env python

from setuptools import setup, find_packages


def readfile(filename):
    with open(filename, 'r') as open_file:
        return open_file.read()


setup(
    name='django-fsm-log',
    version='1.6.2',
    description='Logging for django-fsm',
    long_description=readfile('README.md'),
    long_description_content_type='text/markdown',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/django-fsm-log',
    license='MIT',
    packages=find_packages(),
    install_requires=['django>=1.8', 'django_fsm>=2', 'django_appconf'],
    extras_require={
        'testing': [
            'pytest',
            'pytest-cov',
            'pytest-django',
            'pytest-mock',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
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
