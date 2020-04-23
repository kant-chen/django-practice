"""
Django settings for amazingtalker project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_BASE_DIR = os.environ.get('LOG_BASE_DIR', '/var/log/amazingtalker')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1ed$)hg*=d7alfae9=%#iufx7$=0h8jffewr+mtjlw917gl0#%rl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", True)

ALLOWED_HOSTS = ['127.0.0.1']

# Get database name/user from environmental variables
DEV_DB_NAME = os.environ.get('POSTGRES_DB', 'amazingtalker_default')
DEV_DB_USER_NAME = os.environ.get(
    'POSTGRES_USER', 'amazingtalker_default_user')
DEV_DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')
DEV_DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'apps.user',
    'apps.wallet',
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


ROOT_URLCONF = 'amazingtalker.urls'

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

WSGI_APPLICATION = 'amazingtalker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DEV_DB_NAME,
        'USER': DEV_DB_USER_NAME,
        'PASSWORD': DEV_DB_PASSWORD,
        'HOST': DEV_DB_HOST,
        'PORT': 5432,
        'CONN_MAX_AGE': 0,
        'TEST': {
            'NAME': 'default_amazingtalker_testdb',
            'HOST': DEV_DB_HOST,
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = ['social_core.backends.google.GoogleOAuth2',
                           'django.contrib.auth.backends.ModelBackend',
                           ]
# Oauth2 Google Login settings
LOGIN_URL = '/user/login/google-oauth2/'
LOGIN_REDIRECT_URL = '/main'
LOGOUT_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '548519335291-lb7hdn5l847cva9sd0vdtddjggvmu6la.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'sWcZieXcnuVOzPkorKU_t8B4'

# Oauth2 Facebook Login settings
SOCIAL_AUTH_FACEBOOK_OAUTH2_KEY = "237482420832383"
SOCIAL_AUTH_FACEBOOK_OAUTH2_SECRET = ""
# rest_framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# set custom user model
AUTH_USER_MODEL = 'user.CustomUser'

# Logger handler
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_BASE_DIR+'/debug.log',
        },
        'critical': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_BASE_DIR+'/errors.log',
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['debug', 'critical'],
            'propagate': True
        },
    }
}


# email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = "postmaster@sandbox07b966bce9634412b2a2ace7e90e6437.mailgun.org"
EMAIL_HOST_PASSWORD = "542a3dd9f89e03910ae8583506f339df-4a62b8e8-aa748fc1"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER_NAME = "Kant Chen"
EMAIL_MAILGUN_API_KEY = "2b36b51131f1ee8c51fd8f15f219c2df-4a62b8e8-d5a7b49f"
