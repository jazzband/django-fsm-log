Django Finite State Machine Log
==============

Automatic logging for the excellent [Django FSM](https://github.com/kmmbvnr/django-fsm)
package.


## Installation

First, install the package with pip. This will automatically install any
dependencies you may be missing
```bash
pip install git+https://github.com/gizmag/django-fsm-log.git#egg=django-fsm-log
```

Then migrate the app to create the database table
```bash
python manage.py migrate django_fsm_log
```

## Usage

This app will listen for the `django_fsm.signals.post_transition` to be fired
and create a new record for each transition. To query logs simply
```python
from django_fsm_log.models import StateLog
StateLog.objects.all()
# ...all recorded logs...
```
