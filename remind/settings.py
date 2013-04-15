# coding: UTF-8

from os.path import abspath, dirname, join, normpath
from os import environ
import django.conf.global_settings as DEFAULT_SETTINGS
import os

PROJECT_DIR = dirname(abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME'      : 'remind',                      # Or path to database file if using sqlite3.
        'USER'      : 'root',                      # Not used with sqlite3.
        'PASSWORD'  : '@m4st3r',                  # Not used with sqlite3.
        'HOST'      : 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT'      : '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

ALLOWED_HOSTS = []
TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'
SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = normpath(join(PROJECT_DIR, 'media'))
MEDIA_URL = '/media/'
STATIC_ROOT = normpath(join(PROJECT_DIR, 'public'))
STATIC_URL = '/static/' 


# Additional locations of static files
TEMPLATE_DIRS = (os.path.join(PROJECT_DIR, 'templates'),)
FIXTURE_DIRS = (os.path.join(PROJECT_DIR, 'fixtures'),)
STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g2=6%^rr42)t(!rwfbz2o&amp;xx2r-x!nzb)mi(qhrjw@a)!u#ez^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'remind.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'remind.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    
    'remind.core'
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
