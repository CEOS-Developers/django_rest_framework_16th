from .base import *  # noqa

MyUser = True
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
DEBUG = env('DEBUG')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}