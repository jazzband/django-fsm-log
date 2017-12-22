from functools import wraps, partial
from .helpers import FSMLogAttr


def fsm_log_by(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        arg_list = list(args)
        instance = arg_list.pop(0)

        meta_by = FSMLogAttr(instance, 'by')
        if kwargs.get('by', False):
            meta_by.set(kwargs['by'])
            # kwargs['by'] = meta_by
            instance.by = kwargs['by'] # legacy
            
        out = func(instance, *arg_list, **kwargs)
        
        if kwargs.get('by', False):
            delattr(instance, 'by')
            
        meta_by.remove()

        return out

    return wrapped


def fsm_log_description(func=None, allow_inline=False):
    if func is None:
        return partial(fsm_log_description, allow_inline=allow_inline)

    @wraps(func)
    def wrapped(*args, **kwargs):
        arg_list = list(args)
        instance = arg_list.pop(0)

        meta_description = FSMLogAttr(instance, 'description')
        if kwargs.get('description', False):
            meta_description.set(kwargs['description'])

        if allow_inline or kwargs.get('description', False):
            kwargs['description'] = meta_description

        out = func(instance, *arg_list, **kwargs)

        meta_description.remove()

        return out

    return wrapped
