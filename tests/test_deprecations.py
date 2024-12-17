import pytest


def test_state_log_model():
    from django_fsm_log.models import StateLog

    with pytest.deprecated_call():
        StateLog()


def test_state_log_queryset():
    from django_fsm_log.managers import StateLogQuerySet

    with pytest.deprecated_call():
        StateLogQuerySet()


def test_state_log_manager():
    from django_fsm_log.managers import StateLogManager

    with pytest.deprecated_call():
        StateLogManager()


def test_pending_state_log_manager():
    from django_fsm_log.managers import PendingStateLogManager

    with pytest.deprecated_call():
        PendingStateLogManager()
