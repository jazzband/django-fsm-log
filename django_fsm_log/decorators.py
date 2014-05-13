from functools import wraps


def fsm_log_by(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        arg_list = list(args)
        instance = arg_list.pop(0)

        if kwargs.get('by', False):
            instance.by = kwargs['by']

        out = func(instance, *arg_list, **kwargs)

        if kwargs.get('by', False):
            delattr(instance, 'by')

        return out

    return wrapped
