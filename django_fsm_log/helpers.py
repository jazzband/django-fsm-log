NotSet = object()

class FSMLogAttr(object):

    ATTR_PREFIX = '_django_fsm_log_attr_'
    
    def __init__(self, instance, attribute, value=NotSet):
        self.instance = instance
        self.attribute = "{}{}".format(self.ATTR_PREFIX, attribute)
        if value is not NotSet:
            self.set(value)

    def get(self):
        return getattr(self.instance, self.attribute, None)

    def set(self, value):
        setattr(self.instance, self.attribute, value)

    def remove(self):
        if hasattr(self.instance, self.attribute):
            delattr(self.instance, self.attribute)
