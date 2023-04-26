# Django Finite State Machine Log

[![test suite](https://github.com/jazzband/django-fsm-log/actions/workflows/test_suite.yml/badge.svg)](https://github.com/jazzband/django-fsm-log/actions/workflows/test_suite.yml)
[![codecov](https://codecov.io/gh/jazzband/django-fsm-log/branch/master/graph/badge.svg)](https://codecov.io/gh/jazzband/django-fsm-log)
[![Jazzband](https://jazzband.co/static/img/badge.svg)](https://jazzband.co/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/jazzband/django-fsm-log/master.svg)](https://results.pre-commit.ci/latest/github/jazzband/django-fsm-log/master)
[![Documentation Status](https://readthedocs.org/projects/django-fsm-log/badge/?version=latest)](https://django-fsm-log.readthedocs.io/en/latest/?badge=latest)

Provides persistence of the transitions of your fsm's models. Backed by the excellent [Django FSM](https://github.com/viewflow/django-fsm)
package.

Logs can be accessed before a transition occurs and before they are persisted to the database
by enabling a cached backend. See [Advanced Usage](#advanced-usage)

## Changelog

## 4.0.0 (not released)

- remove support for django 2.2 & 4.0
- Bring your own PersistedTransition model:
  From this release, django-fsm-log is deprecating StateLog and instead encourages you
  to define the concrete model for your own application that will persist the transition.

## 3.1.0 (2023-03-23)

- `fsm_log_description` now accepts a default description parameter
- Document `fsm_log_description` decorator
- Add support for Django 4.1
- Add compatibility for python 3.11

### 3.0.0 (2022-01-14)

- Switch to github actions (from travis-ci)
- Test against django 3.2 and 4.0, then python 3.9 and 3.10
- Drop support for django 1.11, 2.0, 2.1, 3.0, 3.1
- Drop support for python 3.4, 3.5, 3.6
- allow using StateLogManager in migrations [#95](https://github.com/jazzband/django-fsm-log/pull/95)

### 2.0.1 (2020-03-26)

- Add support for django3.0
- Drop support for python2

### 1.6.2 (2019-01-06)

- Address Migration history breakage added in 1.6.1

### 1.6.1 (2018-12-02)

- Make StateLog.description field nullable

### 1.6.0 (2018-11-14)

- Add source state on transitions
- Fixed `get_state_display` with FSMIntegerField (#63)
- Fixed handling of transitions if target is None (#71)
- Added `fsm_log_description` decorator (#1, #67)
- Dropped support for Django 1.10 (#64)

### 1.5.0 (2017-11-29)

- cleanup deprecated code.
- add codecov support.
- switch to pytest.
- add Admin integration to visualize past transitions.

### 1.4.0 (2017-11-09)

- Bring compatibility with Django 2.0 and drop support of unsupported versions
  of Django: `1.6`, `1.7`, `1.9`.

### Compatibility

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

### Define you own model

```python
from django_fsm_log.models import PersistedTransitionMixin


class TransitionLog(PersistedTransitionMixin):
    pass
```

### Register the model

```python
DJANGO_FSM_LOG_CONCRETE_MODEL = 'poll.models.TransitionLog'  # This model must inherit from django_fsm_log.models.PersistedTransition
```

The app listens for the `django_fsm.signals.post_transition` signal and
creates a new record for each transition.

To query the log:

```python
TransitionLog.objects.all()
# ...all recorded logs...
```

### Disabling logging for specific models

By default transitions get recorded for all models. Logging can be disabled for
specific models by adding their fully qualified name to `DJANGO_FSM_LOG_IGNORED_MODELS`.

```python
DJANGO_FSM_LOG_IGNORED_MODELS = ('poll.models.Vote',)
```

### `for_` Manager Method

For convenience there is a custom `for_` manager method to easily filter on the generic foreign key:

```python
from my_app.models import Article

article = Article.objects.all()[0]

TransitionLog.objects.for_(article)
# ...logs for article...
```

### `by` Decorator

We found that our transitions are commonly called by a user, so we've added a
decorator to make logging this easy:

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

With this the transition gets logged when the `by` kwarg is present.

```python
article = Article.objects.create()
article.submit(by=some_user)  # TransitionLog.by will be some_user
```

### `description` Decorator

Decorator that allows to set a custom description (saved on database) to a transitions.

```python
from django.db import models
from django_fsm import FSMField, transition
from django_fsm_log.decorators import fsm_log_description

class Article(models.Model):

    state = FSMField(default='draft', protected=True)

    @fsm_log_description(description='Article submitted')  # description param is NOT required
    @transition(field=state, source='draft', target='submitted')
    def submit(self, description=None):
        pass

article = Article.objects.create()
article.submit()  # logged with "Article submitted" description
article.submit(description="Article reviewed and submitted")  # logged with "Article reviewed and submitted" description
```

.. TIP::
    The "description" argument passed when calling ".submit" has precedence over the default description set in the decorator

The decorator also accepts a `allow_inline` boolean argument that allows to set the description inside the transition method.

```python
from django.db import models
from django_fsm import FSMField, transition
from django_fsm_log.decorators import fsm_log_description

class Article(models.Model):

    state = FSMField(default='draft', protected=True)

    @fsm_log_description(allow_inline=True)
    @transition(field=state, source='draft', target='submitted')
    def submit(self, description=None):
        description.set("Article submitted")

article = Article.objects.create()
article.submit()  # logged with "Article submitted" description
```

### Admin integration

There is an InlineForm available that can be used to display the history of changes.

To use it expand your own `AdminModel` by adding `PersistedTransitionInline` to its inlines:

```python
from django.contrib import admin
from django_fsm_log.admin import PersistedTransitionInline


@admin.register(FSMModel)
class FSMModelAdmin(admin.ModelAdmin):
    inlines = [PersistedTransitionInline]
```

### Migration to Abstract model PersistedTransitionMixin

Once you defined your own model, you'll have to create the relevant migration to create the table.

```sh
python manage.py makemigrations
```

Additionally you'd want to migrate the data from django_fsm_log.models.StateLog to your new table.

### Advanced Usage

You can change the behaviour of this app by turning on caching for PersistedTransition records.
Simply add `DJANGO_FSM_LOG_STORAGE_METHOD = 'django_fsm_log.backends.CachedBackend'` to your project's settings file.
It will use your project's default cache backend by default. If you wish to use a specific cache backend, you can add to
your project's settings:

```python
DJANGO_FSM_LOG_CACHE_BACKEND = 'some_other_cache_backend'
```

The PersistedTransition object is now available after the `django_fsm.signals.pre_transition`
signal is fired, but is deleted from the cache and persisted to the database after `django_fsm.signals.post_transition`
is fired.

This is useful if:

- you need immediate access to PersistedTransition details, and cannot wait until `django_fsm.signals.post_transition`
has been fired
- at any stage, you need to verify whether or not the PersistedTransition has been written to the database

Access to the pending PersistedTransition record is available via the `pending_objects` manager

```python
from my_app.models import TransitionLog

article = Article.objects.get(...)
pending_transition_logs = TransitionLog.pending_objects.get_for_object(article)
```

## Contributing

### Running tests

```bash
pip install tox
tox
```

### Linting with pre-commit

We use ruff, black and more, all configured and check via [pre-commit](https://pre-commit.com/).
Before committing, run the following:

```bash
pip install pre-commit
pre-commit install
```
