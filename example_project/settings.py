# Django settings for fsm_log project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_fsm_log',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '',
        'PORT': '',
    }
}

USE_TZ = True
SECRET_KEY = 'p7))nc%7nj5iq_l#gm52&^37m(bg^c5(mo+rs=md9ss*5tg+*h'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'south',
    'django_fsm_log',
)
