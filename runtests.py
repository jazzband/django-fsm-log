#!/usr/bin/env python
import os
import sys

from django.conf import settings
from django.core.management import execute_from_command_line


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        USE_TZ=True,
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'south',
            'django_fsm_log',
            'tests',
        ),
        TEST_RUNNER='django_nose.NoseTestSuiteRunner',
    )


def runtests():
    argv = sys.argv[:1] + ['test', 'tests']
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
