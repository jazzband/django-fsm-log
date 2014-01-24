Django Finite State Machine Log
==============

[![Build Status](https://travis-ci.org/gizmag/django-fsm-log.png?branch=master)](https://travis-ci.org/gizmag/django-fsm-log)
[![Code Health](https://landscape.io/github/gizmag/django-fsm-log/master/landscape.png)](https://landscape.io/github/gizmag/django-fsm-log/master)

Automatic logging for the excellent [Django FSM](https://github.com/kmmbvnr/django-fsm)
package.


## Installation

First, install the package with pip. This will automatically install any
dependencies you may be missing
```bash
pip install django-fsm-log
```

With Python 2.7 Django 1.4+ is supported, with Python 3.3 Django 1.5+ is supported.

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
from django_fsm.db.fields import FSMField, transition
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


### Advanced Usage
You can change the behaviour of this app by turning on caching for StateLog records.
Simply add `DJANGO_FSM_LOG_CACHE_BACKEND = 'backend_name'` to your project's settings file. This
will store any pending StateLog records in the cache using the cache backend you specified.

This is useful if you need to verify whether or not the StateLog has been written to the database.
Access to the pending StateLog record is available via the `pending_objects` manager

```python
from django_fsm_log.models import StateLog
article = Article.objects.get(...)
pending_state_log = StateLog.pending_objects.get_for_object(article)
```

This pending StateLog object is available after the `django_fsm.signals.pre_transition`
signal is fired, but is deleted from the cache after `django_fsm.signals.post_transition`
is fired.

## Running Tests

```
./runtests.py
```
