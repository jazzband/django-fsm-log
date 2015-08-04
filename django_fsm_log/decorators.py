from functools import wraps

def fsm_log_by(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        arg_list = list(args)
        instance = arg_list.pop(0)

        if kwargs.get('by', False):
            instance.by = kwargs['by']
            
        if kwargs.get('description', False):
            instance.description = kwargs['description']

        out = func(instance, *arg_list, **kwargs)

        if kwargs.get('by', False):
            delattr(instance, 'by')

        if kwargs.get('description', False):
            delattr(instance, 'description')

        return out

    return wrapped
