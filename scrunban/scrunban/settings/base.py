"""
Django settings for srumban project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from scrunban.settings.secret_config import *

# Application definition

PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'guardian',
]

PROJECT_APPS = [
    'apps.autenticacion',
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'scrunban.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.abspath(os.path.join(BASE_DIR, "../templates/")),
        ],
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

WSGI_APPLICATION = 'scrunban.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../statics/"))

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.abspath(os.path.join(BASE_DIR, "../static/"))
]

# CONFIGURACIÓN DE LOGIN!!
URL_NAME_FORMAT = '{}_{}'
APP_NAME_AUTENTICACION = 'auth' #TODO NO CAMBIAR!!
LOGIN_NAME  = URL_NAME_FORMAT.format( APP_NAME_AUTENTICACION, 'name')
AUTH_NAME   = URL_NAME_FORMAT.format( APP_NAME_AUTENTICACION, 'auth')
DEAUTH_NAME = URL_NAME_FORMAT.format( APP_NAME_AUTENTICACION, 'deauth')

PERFIL_NAME = URL_NAME_FORMAT.format( APP_NAME_AUTENTICACION, 'perfil')

PROJECT_ROLE_LIST = URL_NAME_FORMAT.format( APP_NAME_AUTENTICACION, 'role_list')
PROJECT_ROLE_CREATE = URL_NAME_FORMAT.format( APP_NAME_AUTENTICACION, 'role_create_delete')
PROJECT_ROLE_DELETE = URL_NAME_FORMAT.format( APP_NAME_AUTENTICACION, 'role_delete')
PROJECT_ROLE_DETAIL = URL_NAME_FORMAT.format( APP_NAME_AUTENTICACION, 'role_detail')
PROJECT_ROLE_EDIT = URL_NAME_FORMAT.format( APP_NAME_AUTENTICACION, 'role_edit')

URL_NAMES = {
    'LOGIN_NAME': LOGIN_NAME,
    'AUTH_NAME': AUTH_NAME,
    'DEAUTH_NAME': DEAUTH_NAME,
    'PERFIL_NAME': PERFIL_NAME,
    'PROJECT_ROLE_LIST': PROJECT_ROLE_LIST,
    'PROJECT_ROLE_CREATE': PROJECT_ROLE_CREATE,
    'PROJECT_ROLE_DELETE': PROJECT_ROLE_DELETE,
    'PROJECT_ROLE_DETAIL': PROJECT_ROLE_DETAIL,
    'PROJECT_ROLE_EDIT': PROJECT_ROLE_EDIT,

}