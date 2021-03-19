# Development settings
import os

from .base import *

SECRET_KEY = ')x^tnrs^yggo!s+-@9o#na%l)26q@*rsyco^pdq0w(eqvuyxj*'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'foodacademy',
        'USER': 'foodacademyadmin',
        'PASSWORD': 'Fo0ac@demyA&min1',
        'HOST': 'db',
        'PORT': '5432'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'tmp/contactus/email/'
ADMIN_EMAIL = 'nikita@selin.com.ru'
