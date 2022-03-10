"""
Django settings for g4growth project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import environ
from pathlib import Path
import os

#initializing environment 
env = environ.Env()
environ.Env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wb2*ep&kicc)#h_#s_)57rzg12@$!7jxmh-m@gonm0@q9p#$6)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '*', 'http://g4growth.chppukqmi3c6.ap-south-1.rds.amazonaws.com/']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "http://www.g4growth.com" , "http://api.g4growth.com"
]

CORS_ALLOW_METHODS = [
'GET',
'OPTIONS',
'POST'
]
# Application definition
CORS_ALLOW_CREDENTIALS = True
INSTALLED_APPS = [
    'django_crontab',
    'user',
    'courses',
    'credit',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'g4growth.urls'

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

WSGI_APPLICATION = 'g4growth.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'g4growth_db',
        'USER': 'admin',
        'PASSWORD': '5BlQFWShWe4zCOrxYer2',
        'HOST': 'g4growth.chppukqmi3c6.ap-south-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'images'),
# ]

AWS_ACCESS_KEY_ID = 'AKIA6MATVUNHQTFOPPNF'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'g4growth-courses'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_STATIC_LOCATION = 'static'
AWS_PUBLIC_MEDIA_LOCATION = 'courses/public'
AWS_PUBLIC_MEDIA_LOCATION2 = 'profile_images'
AWS_PRIVATE_MEDIA_LOCATION = 'courses/private'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)
STATICFILES_STORAGE = 'g4growth.storage_backends.StaticStorage'
DEFAULT_FILE_STORAGE = 'g4growth.storage_backends.MediaStorage'
PRIVATE_FILE_STORAGE = 'g4growth.storage_backends.PrivateMediaStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# STATICFILES_DIRS = ['/images/']

CRONJOBS = [
    ('*/1 * * * *', 'g4growth.cron.delete_expired'),
    ('*/3 * * * *', 'g4growth.cron.add_credit'),
]
