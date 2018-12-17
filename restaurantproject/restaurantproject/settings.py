"""
Django settings for restaurantproject project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'eam6a2=62-4791^o-z0z+*xhjk$3^w@9$4v4a2#96%y-cnftdj'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# TODO: Naci bolju alternativu.
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '10.99.161.122',
    '10.99.177.11',
    '10.99.161.97',
    '10.99.178.129',
    '10.99.161.122'
]

# TODO: Ovo nije bolja alternativa.
# ALLOWED_HOSTS += ['192.168.{}.{}'.format(i,j) for i in range(256) for j in range(256)]
# ALLOWED_HOSTS += ['10.{}.{}.{}'.format(i,j,k) for i in range(256) for j in range(256) for k in range(256)]
# ALLOWED_HOSTS += ['172.{}.{}.{}'.format(i,j,k) for i in range(16,32) for j in range(256) for k in range(256)]


# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'guest.apps.GuestConfig',
    'bartender.apps.BartenderConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restaurantproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'restaurantproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# TODO: Podesiti PostgreSQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'NAME': os.path.join(BASE_DIR, 'db.postgresql'),
        # 'USER': 'user',
        # 'PASSWORD': 'password',
        # 'HOST': '127.0.0.1',
        # 'PORT': '8000',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# TODO: Podesiti na nas?
LANGUAGE_CODE = 'en-us'

# TODO: Podesiti na nasu?
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# TODO: Ne bi trebalo vaziti za sve pristupe?
LOGIN_REDIRECT_URL = 'bartender-orders'