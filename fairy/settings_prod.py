import os

from fairy.settings import *  # noqa

DEBUG = False
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.getenv('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_DRIVER', 'django.db.backends.postgresql_psycopg2'),
        'NAME': os.getenv('DB_NAME', 'fairy'),
        'USER': os.getenv('DB_USER', 'fairy'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432')
    }
}
