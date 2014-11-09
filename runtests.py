#!/usr/bin/env python
import sys

from django.conf import settings
from django.core.management import execute_from_command_line


apps = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_fsm_log',
    'tests',
]

try:
    import south
except:
    pass
else:
    apps.append('south')

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        USE_TZ=True,
        INSTALLED_APPS=apps,
        MIDDLEWARE_CLASSES=()
    )


def runtests():
    argv = sys.argv[:1] + ['test', 'tests']
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
