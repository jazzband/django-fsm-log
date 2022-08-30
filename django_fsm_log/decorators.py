from functools import partial, wraps

from .helpers import FSMLogDescriptor


def fsm_log_by(func):
    """Set the "by" field of a transition.

    :param func: transition method
    :type func: function
    """

    @wraps(func)
    def wrapped(instance, *args, **kwargs):
        try:
            by = kwargs["by"]
        except KeyError:
            return func(instance, *args, **kwargs)
        with FSMLogDescriptor(instance, "by", by):
            return func(instance, *args, **kwargs)

    return wrapped


def fsm_log_description(func=None, allow_inline=False, description=None):
    """Set the "description" field of a transition.

    :param func: transition method, defaults to None
    :type func: function, optional
    :param allow_inline: allow to set the description inside the transition method, defaults to False
    :type allow_inline: bool, optional
    :param description: default description, defaults to None
    :type description: str, optional
    """
    if func is None:
        return partial(fsm_log_description, allow_inline=allow_inline, description=description)

    @wraps(func)
    def wrapped(instance, *args, **kwargs):
        with FSMLogDescriptor(instance, "description") as descriptor:
            if kwargs.get("description"):
                descriptor.set(kwargs["description"])
            elif allow_inline:
                kwargs["description"] = descriptor
            else:
                descriptor.set(description)
            return func(instance, *args, **kwargs)

    return wrapped
