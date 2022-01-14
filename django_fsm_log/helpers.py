NOTSET = object()


class FSMLogDescriptor:

    ATTR_PREFIX = "__django_fsm_log_attr_"

    def __init__(self, instance, attribute, value=NOTSET):
        self.instance = instance
        self.attribute = attribute
        if value is not NOTSET:
            self.set(value)

    def get(self):
        return getattr(self.instance, self.ATTR_PREFIX + self.attribute)

    def set(self, value):
        setattr(self.instance, self.ATTR_PREFIX + self.attribute, value)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        try:
            delattr(self.instance, self.ATTR_PREFIX + self.attribute)
        except AttributeError:
            pass
