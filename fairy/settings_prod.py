import os

from fairy.settings import *  # noqa

DEBUG = False
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.getenv('SECRET_KEY')
SECURE_HSTS_SECONDS = 604800
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# 
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'


DATABASES['default'] = {  # noqa
    'ENGINE': os.getenv('DB_DRIVER', 'django.db.backends.postgresql_psycopg2'),
    'NAME': os.getenv('DB_NAME', 'fairy'),
    'USER': os.getenv('DB_USER', 'fairy'),
    'PASSWORD': os.getenv('DB_PASSWORD'),
    'HOST': os.getenv('DB_HOST', 'localhost'),
    'PORT': os.getenv('DB_PORT', '5432'),
}
