"""
Django settings for fetch_metadata project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from decouple import config
import django_on_heroku
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "DJANGO_SECRET_KEY"

DJANGO_ALLOWED_HOSTS = ["localhost", "metatrack.herokuapp.com", "*.metatrack.herokuapp.com"]
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = DJANGO_ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

     # 3rd Party
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    # 'crispy_forms',

    #local apps
    'api.apps.ApiConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.commons.apps.CommonsConfig',
    'apps.file_control.apps.FileControlConfig',
]

AUTH_USER_MODEL = 'accounts.CustomUser'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # During development only

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fetch_metadata.urls'
CSRF_TRUSTED_ORIGINS = [
    'https://metatrack.herokuapp.com'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR/"templates",
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

WSGI_APPLICATION = 'fetch_metadata.wsgi.application'



#decouple database variables from .env
PG_DB = config("PG_DB")
PG_USER = config("PG_USER")
PG_PASSWORD = config("PG_PASSWORD")
PG_HOST = config("PG_HOST")
PG_PORT = config("PG_PORT")

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PG_DB,
        'USER': PG_USER,
        'PASSWORD': PG_PASSWORD,
        'HOST': PG_HOST,
        'PORT': PG_PORT,
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

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#### REST_FRAME_WORK_SETTINGS#####
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES':[
                'rest_framework.permissions.IsAuthenticated',
    ],
}
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "home"

# Configure Django App for Heroku
if DEBUG is False:
    import django_on_heroku
    import dj_database_url
    STATIC_URL = '/fetchmetadata.s3.af-south-1.amazonaws.com/'
    MEDIA_URL = '/fetchmetadata.s3.af-south-1.amazonaws.com/'


    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = config("AWS_S3_CUSTOM_DOMAIN")
    AWS_S3_REGION_NAME = "af-south-1"
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL=None

    # AWS_CLOUDFRONT_KEY = config('AWS_CLOUDFRONT_KEY', None).encode('ascii')
    # AWS_CLOUDFRONT_KEY_ID = config('AWS_CLOUDFRONT_KEY_ID', None)
    AWS_LOCATION = 'media'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'staticdev'),
    ]
    STATIC_ROOT = 'static'

    MEDIA_ROOT = 'media'
    if "localhost" not in DJANGO_ALLOWED_HOSTS:
        django_on_heroku.settings(locals())

        DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

else:
    #Media files (uploaded files)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STATIC_ROOT = 'static'


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/

    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'staticdev')
        ]
    
    
django_on_heroku.settings(locals())
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

