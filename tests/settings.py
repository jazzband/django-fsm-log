DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3'}
}
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_fsm_log',
    'tests',
]
MIDDLEWARES = []
MIDDLEWARE_CLASSES = []
SECRET_KEY = 'abc123'
