#!/usr/bin/env python

from setuptools import find_packages, setup


def readfile(filename):
    with open(filename) as open_file:
        return open_file.read()


setup(
    name="django-fsm-log",
    version="4.0.0.dev0",
    description="Transition's persistence for django-fsm",
    long_description=readfile("README.md"),
    long_description_content_type="text/markdown",
    author="Gizmag",
    author_email="tech@gizmag.com",
    url="https://github.com/jazzband/django-fsm-log",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    install_requires=["django>=3.2", "django-fsm-2", "django_appconf"],
    extras_require={
        "testing": [
            "pytest",
            "pytest-cov",
            "pytest-django",
            "pytest-mock",
        ],
        "docs": [
            "sphinx",
            "sphinx_rtd_theme",
            "myst-parser",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
