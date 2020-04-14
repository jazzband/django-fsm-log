import ast
import inspect

import django
from django.core.checks import (
    Warning,
    register,
    Tags,
)
from django.core.exceptions import FieldDoesNotExist


@register(Tags.compatibility)
def integer_object_id_check(app_configs, **kwargs):
    errors = []
    for app in django.apps.apps.get_app_configs():

        # Skip third party apps.
        if app.path.find('site-packages') > -1:
            continue

        for model in app.get_models():
            for check_message in check_model_for_integer_object_id(model):
                errors.append(check_message)
    return errors


def check_model_for_integer_object_id(model):
    """Check a single model.

    Yields (django.checks.CheckMessage)
    """

    from django_fsm_log.models import StateLog

    model_source = inspect.getsource(model)
    model_node = ast.parse(model_source)

    for node in model_node.body[0].body:

        # Check if node is a model field.
        if not isinstance(node, ast.Assign):
            continue

        if len(node.targets) != 1:
            continue

        if not isinstance(node.targets[0], ast.Name):
            continue

        field_name = node.targets[0].id
        try:
            field = model._meta.get_field(field_name)
        except FieldDoesNotExist:
            continue

        # Node is a model field here

        # Check if field has foreign key to StateLog defined
        for kw in node.value.keywords:
            if kw.arg == 'to':
                to = kw
                if to == 'django_fsm_log.StateLog' or isinstance(to, StateLog):
                    yield Warning(
                        'StateLog has changed its object_id from PositiveIntegerField to TextField to better support '
                        'the primary key types in Django.',
                        hint='Migration PositiveIntegerField -> TextField is potentially needed on field {}.'.format(
                            field.name
                        ),
                        obj=field,
                        id='django_fsm_log.W001',
                    )
