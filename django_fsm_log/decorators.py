from functools import partial, wraps

from .helpers import FSMLogDescriptor


def fsm_log_by(func):
    @wraps(func)
    def wrapped(instance, *args, **kwargs):
        try:
            by = kwargs["by"]
        except KeyError:
            return func(instance, *args, **kwargs)
        with FSMLogDescriptor(instance, "by", by):
            return func(instance, *args, **kwargs)

    return wrapped


def fsm_log_description(func=None, allow_inline=False, description=""):
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
