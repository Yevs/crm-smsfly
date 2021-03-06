"""
Django settings for SMSFlyCRM project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
from django.utils.translation import ugettext_lazy as _

import environ

# Build paths inside the project like this: BASE_DIR(...)
BASE_DIR = environ.Path(__file__) - 2  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(
    DEBUG=(bool, False),
)  # set default values and casting
environ.Env.read_env()  # reading .env file

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'npm.finders.NpmFinder',
    'djangobower.finders.BowerFinder',
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY',
                 default='&#bo9#p#5jbn16!@$tb99hg6sx_ki5yf0)w)s+$ggi#h*wk*=5')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SMSFlyCRM.SMSApp',  # <-- our app
    'SMSFlyCRM.smartselects',  # <-- smart_selects custom views
    # third-party apps:
    'bootstrap3',
    'django_rq',
    'django_rq_jobs',
    'datetimewidget',
    'django_extensions',
    'debug_toolbar',
    'recurrence',
    'smart_selects',
    'djangobower',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'SMSFlyCRM.SMSApp.middleware.iframe.UserInIframeMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SMSFlyCRM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SMSFlyCRM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': env.db(),  # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'crm': env.db('CRM_DB_URL', default='sqlite:///db.sqlite3'),
}

DATABASE_ROUTERS = ['SMSFlyCRM.SMSApp.db_routers.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {'internal_app': 'default',
                         'external_app': 'crm'}


REDIS_URL = env('REDIS_URL', default='redis://localhost:6379/0')

RQ_QUEUES = {
    'default': {
        'URL': REDIS_URL,
        'DEFAULT_TIMEOUT': 500,
    },
    'high': {
        'URL': REDIS_URL,
        'DEFAULT_TIMEOUT': 500,
    },
    'low': {
        'URL': REDIS_URL,
        'DEFAULT_TIMEOUT': 500,
    },
}

RQ_JOBS_MODULE = 'SMSFlyCRM.SMSApp.tasks'


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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'uk-ua'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
  ('uk', _('Ukrainian')),
  ('en', _('English')),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT_DIR = env.path('STATIC_ROOT', BASE_DIR('static'))
STATIC_ROOT = STATIC_ROOT_DIR()

SMS_FLY = {
    'login': env('SMSFLY_ID'),
    'password': env('SMSFLY_PASS'),
}

BOOTSTRAP3 = {
    'javascript_in_head': True,
    'include_jquery': True,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': env.path('DJANGO_DEBUG_LOG', 'log/smsapp.debug.log')(),
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': env('DJANGO_LOG_LEVEL', default='ERROR'),
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': env('DJANGO_LOG_LEVEL', default='ERROR'),
            'propagate': False,
        },
        'smsfly': {
            'handlers': ['console', 'file'],
            'level': env('DJANGO_LOG_LEVEL', default='ERROR'),
            'propagate': False,
        },
        'werkzeug': {
            'handlers': ['console', 'file'],
            'level': env('DJANGO_LOG_LEVEL', default='ERROR'),
            'propagate': True,
        },
        'watchdog': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8000'

# Django Smart Selects:
USE_DJANGO_JQUERY = False
JQUERY_URL = '//about:blank'  # hack around loading jquery to prevent it from breaking datepicker

NPM_ROOT_PATH = BASE_DIR()

NPM_FILE_PATTERNS = {
    # 'angular2': ['*.js', '*.map'],
    # 'es6-shim': ['es6-shim.min.js', 'es6-shim.map'],
    # 'systemjs': ['dist/*.js', '*.map'],
    # 'rxjs': ['bundles/Rx.js', '*.js', '*.map'],
    # 'ng2-material': ['*.css', '*.js', '*.map', '*.ts']
}

NPM_STATIC_FILES_PREFIX = 'js/lib'

# BOWER_COMPONENTS_ROOT = STATIC_ROOT_DIR('js/lib')
BOWER_COMPONENTS_ROOT = BASE_DIR()

BOWER_INSTALLED_APPS = (
    'jquery#1.9',
    'underscore',
    'twbs-pagination',
)
