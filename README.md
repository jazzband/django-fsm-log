Django Finite State Machine Log
==============

[![Build Status](https://travis-ci.org/gizmag/django-fsm-log.png?branch=master)](https://travis-ci.org/gizmag/django-fsm-log)
[![Code Health](https://landscape.io/github/gizmag/django-fsm-log/master/landscape.png)](https://landscape.io/github/gizmag/django-fsm-log/master)
[![codecov](https://codecov.io/gh/gizmag/django-fsm-log/branch/master/graph/badge.svg)](https://codecov.io/gh/gizmag/django-fsm-log)

Automatic logging for the excellent [Django FSM](https://github.com/kmmbvnr/django-fsm)
package.

Logs can be accessed before a transition occurs and before they are persisted to the database
by enabling a cached backend. See [Advanced Usage](#advanced-usage)

## Changelog

- `1.5.0` 2017/11/29

    - cleanup deprecated code.
    - add codecov support.
    - switch to pytest.
    - add Admin integration to visualize past transitions.

- `1.4.0` 2017/11/09

    - Bring compatibility with django 2.0 and drop support of unsupported versions of Django: `1.6`, `1.7`, `1.9`.

### Compatability

- Python 2.7 and 3.4+
- Django 1.8+
- Django-FSM 2+

## Installation

First, install the package with pip. This will automatically install any
dependencies you may be missing
```bash
pip install django-fsm-log
```

Register django_fsm_log in your list of Django applications:

```python
INSTALLED_APPS = (
    ...,
    'django_fsm_log',
    ...,
)
```

Then migrate the app to create the database table
```bash
python manage.py migrate django_fsm_log
```

## Usage
The app will listen for `django_fsm.signals.post_transition` to be fired and
create a new record for each transition.

To query logs simply
```python
from django_fsm_log.models import StateLog
StateLog.objects.all()
# ...all recorded logs...
```

### Disabling logging for specific models

By default transitions are logged for all models. Logging can be disabled for
specific models by adding their fully qualified name to `DJANGO_FSM_LOG_IGNORED_MODELS`.

```python
DJANGO_FSM_LOG_IGNORED_MODELS = ('poll.models.Vote')
```

### `for_` Manager Method

For convenience there is a custom `for_` manager method to easily filter on the generic foreign key
```python
from my_app.models import Article
from django_fsm_log.models import StateLog

article = Article.objects.all()[0]

StateLog.objects.for_(article)
# ...logs for article...
```

### `by` Decorator

We found that our transitions are commonly called by a user, so we've added a decorator to make logging that painless

```python
from django.db import models
from django_fsm import FSMField, transition
from django_fsm_log.decorators import fsm_log_by

class Article(models.Model):

    state = FSMField(default='draft', protected=True)

    @fsm_log_by
    @transition(field=state, source='draft', target='submitted')
    def submit(self, by=None):
        pass

```

Then every time the transition is called with the `by` kwarg set, it will be logged

```python
article = Article.objects.create()
article.submit(by=some_user) # StateLog.by will be some_user
```

### Admin integration

There is an InlineForm available that can be used to display the history of changes.

To use it expand your own `AdminModel` by adding `StateLogInline` to its inlines:

```python
from django.contrib import admin
from django_fsm_log.admin import StateLogInline


@admin.register(FSMModel)
class FSMModel(admin.ModelAdmin):
    inlines = [StateLogInline]
```
### Advanced Usage
You can change the behaviour of this app by turning on caching for StateLog records.
Simply add `DJANGO_FSM_LOG_STORAGE_METHOD = 'django_fsm_log.backends.CachedBackend'` to your project's settings file.
It will use your project's default cache backend by default. If you wish to use a specific cache backend, you can add to
your project's settings:
```python
DJANGO_FSM_LOG_CACHE_BACKEND = 'some_other_cache_backend'
```

The StateLog object is now available after the `django_fsm.signals.pre_transition`
signal is fired, but is deleted from the cache and persisted to the database after `django_fsm.signals.post_transition`
is fired.

This is useful if:
- you need immediate access to StateLog details, and cannot wait until `django_fsm.signals.post_transition`
has been fired
- at any stage, you need to verify whether or not the StateLog has been written to the database

Access to the pending StateLog record is available via the `pending_objects` manager

```python
from django_fsm_log.models import StateLog
article = Article.objects.get(...)
pending_state_log = StateLog.pending_objects.get_for_object(article)
```


## Running Tests

```bash
$ pip install tox
$ tox
```
