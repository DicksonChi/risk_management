"""Django settings for risk_management project."""

import os
import environ
# Load operating system environment variables and then prepare to use them
ENV = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


ALLOWED_HOSTS = ['localhost:',
                 '127.0.0.1',
                 'https://qv05nxyeec.execute-api.eu-west-3.amazonaws.com']

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (

    'google.com',
    'hostname.example.com',
    'localhost:8000',
    '127.0.0.1:8000'

)


# Application definition

INSTALLED_APPS = [
    # Dependencies
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django_extensions',
    'django.contrib.staticfiles',
    'zappa_django_utils',

    # App
    'main',

    # rest-framework
    'rest_framework',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'risk_management.urls'

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

REST_FRAMEWORK = {
    # other settings...

    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}

WSGI_APPLICATION = 'risk_management.wsgi.application'
AUTH_USER_MODEL = 'main.User'
AUTH_PASSWORD_VALIDATORS = []


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# fixtures
FIXTURE_DIR = os.path.join(BASE_DIR, "fixtures")

PAGE_CACHE_SECONDS = 1

# # SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    # 'default': {
    #     # for testing will use postgres when want to o live
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zapdjangodb',
        'USER': 'zapdjangouser',
        'PASSWORD': 'df56cdba-e9f0-403c-b57b-db0e4466cc30',
        'HOST': 'zapdjangodb.czqhim8g0q9a.eu-west-3.rds.amazonaws.com',
        'PORT': 5432,
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# STATIC_ROOT = os.path.join(BASE_DIR, "static")


ALLOWED_HOSTS += ['*']  # NOQA

AWS_S3_BUCKET_NAME_STATIC = "YOUR OWN BUCKET"
AWS_S3_BUCKET_AUTH_STATIC = True
AWS_ACCESS_KEY_ID = "YOUR SECRET KEY"
AWS_SECRET_ACCESS_KEY = "YOUR SECRET KEY"
AWS_REGION = "YOUR REGION"
