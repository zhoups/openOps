"""
Django settings for blueopsserver project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys

import ldap

from django.urls import reverse_lazy


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

sys.path.append(PROJECT_DIR)

# Import project config setting
try:
    from config import config as CONFIG
except ImportError:
    CONFIG = type('_', (), {'__getattr__': lambda arg1, arg2: None})()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.DEBUG or False


# Absolute url for some case, for example email link
SITE_URL = CONFIG.SITE_URL or 'http://localhost'


# LOG LEVEL
LOG_LEVEL = 'DEBUG' if DEBUG else CONFIG.LOG_LEVEL or 'WARNING'

ALLOWED_HOSTS = CONFIG.ALLOWED_HOSTS or []

# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'assets.apps.AssetsConfig',
    'perms.apps.PermsConfig',
    'ops.apps.OpsConfig',
    'common.apps.CommonConfig',
    'terminal.apps.TerminalConfig',
    'machine.apps.MachineConfig',
    'rest_framework',
    'rest_framework_swagger',
    'django_filters',
    'bootstrap3',
    'captcha',
    'django_celery_beat',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blueops.middleware.TimezoneMiddleware',
    'blueops.middleware.DemoMiddleware',
]

ROOT_URLCONF = 'blueops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'blueops.context_processor.blueops_processor',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
            ],
        },
    },
]

# WSGI_APPLICATION = 'jumpserver.wsgi.applications'

LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGIN_URL = reverse_lazy('users:login')

SESSION_COOKIE_DOMAIN = CONFIG.SESSION_COOKIE_DOMAIN or None
CSRF_COOKIE_DOMAIN = CONFIG.CSRF_COOKIE_DOMAIN or None
SESSION_COOKIE_AGE = CONFIG.SESSION_COOKIE_AGE or 3600*24

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(CONFIG.DB_ENGINE),
        'NAME': CONFIG.DB_NAME,
        'HOST': CONFIG.DB_HOST,
        'PORT': CONFIG.DB_PORT,
        'USER': CONFIG.DB_USER,
        'PASSWORD': CONFIG.DB_PASSWORD,
        'ATOMIC_REQUESTS': True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
#
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

# Logging setting
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'main': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(module)s %(levelname)s] %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'main',
            'filename': os.path.join(CONFIG.LOG_DIR, 'blueops.log')
        },
        'ansible_logs': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'main',
            'filename': os.path.join(PROJECT_DIR, 'logs', 'ansible.log')
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': LOG_LEVEL,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'blueops': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
        },
        'blueops.users.api': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
        },
        'blueops.users.view': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
        },
        'ops.ansible_api': {
            'handlers': ['console', 'ansible_logs'],
            'level': LOG_LEVEL,
        },
        'django_auth_ldap': {
            'handlers': ['console', 'ansible_logs'],
            'level': "INFO",
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# I18N translation
LOCALE_PATHS = [os.path.join(BASE_DIR, 'i18n'), ]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, "data", "static")
STATIC_DIR = os.path.join(BASE_DIR, "static")


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Media files (File, ImageField) will be save these

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'data', 'media').replace('\\', '/') + '/'

# Use django-bootstrap-form to format template, input max width arg
# BOOTSTRAP_COLUMN_COUNT = 11

# Init data or generate fake data source for development
FIXTURE_DIRS = [os.path.join(BASE_DIR, 'fixtures'),]

# Email config
EMAIL_HOST = CONFIG.EMAIL_HOST
EMAIL_PORT = CONFIG.EMAIL_PORT
EMAIL_HOST_USER = CONFIG.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = CONFIG.EMAIL_HOST_PASSWORD
EMAIL_USE_SSL = CONFIG.EMAIL_USE_SSL
EMAIL_USE_TLS = CONFIG.EMAIL_USE_TLS
EMAIL_SUBJECT_PREFIX = CONFIG.EMAIL_SUBJECT_PREFIX or ''

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'users.permissions.IsSuperUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.AccessKeyAuthentication',
        'users.authentication.AccessTokenAuthentication',
        'users.authentication.PrivateTokenAuthentication',
        'users.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'ORDERING_PARAM': "order",
    'SEARCH_PARAM': "search",
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S %z',
    'DATETIME_INPUT_FORMATS': ['%Y-%m-%d %H:%M:%S %z'],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 15
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Custom User Auth model
AUTH_USER_MODEL = 'users.User'


# Auth LDAP settings
AUTH_LDAP = CONFIG.AUTH_LDAP
AUTH_LDAP_SERVER_URI = CONFIG.AUTH_LDAP_SERVER_URI
AUTH_LDAP_BIND_DN = CONFIG.AUTH_LDAP_BIND_DN
AUTH_LDAP_BIND_PASSWORD = CONFIG.AUTH_LDAP_BIND_PASSWORD
AUTH_LDAP_SEARCH_OU = CONFIG.AUTH_LDAP_SEARCH_OU
AUTH_LDAP_SEARCH_FILTER = CONFIG.AUTH_LDAP_SEARCH_FILTER
AUTH_LDAP_START_TLS = CONFIG.AUTH_LDAP_START_TLS
AUTH_LDAP_USER_ATTR_MAP = CONFIG.AUTH_LDAP_USER_ATTR_MAP
# AUTH_LDAP_USER_SEARCH = LDAPSearch(
#    AUTH_LDAP_SEARCH_OU, ldap.SCOPE_SUBTREE, AUTH_LDAP_SEARCH_FILTER,
# )
AUTH_LDAP_GROUP_SEARCH_OU = CONFIG.AUTH_LDAP_GROUP_SEARCH_OU
AUTH_LDAP_GROUP_SEARCH_FILTER = CONFIG.AUTH_LDAP_GROUP_SEARCH_FILTER
# AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
#     AUTH_LDAP_GROUP_SEARCH_OU, ldap.SCOPE_SUBTREE, AUTH_LDAP_GROUP_SEARCH_FILTER
# )
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_BACKEND = 'django_auth_ldap.backend.LDAPBackend'

if AUTH_LDAP:
    AUTHENTICATION_BACKENDS.insert(0, AUTH_LDAP_BACKEND)


# Celery using redis as broker
CELERY_BROKER_URL = 'redis://:%(password)s@%(host)s:%(port)s/3' % {
    'password': CONFIG.REDIS_PASSWORD if CONFIG.REDIS_PASSWORD else '',
    'host': CONFIG.REDIS_HOST or '127.0.0.1',
    'port': CONFIG.REDIS_PORT or 6379,
}
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_RESULT_EXPIRES = 3600
# CELERY_WORKER_LOG_FORMAT = '%(asctime)s [%(module)s %(levelname)s] %(message)s'
CELERY_WORKER_LOG_FORMAT = '%(message)s'
# CELERY_WORKER_TASK_LOG_FORMAT = '%(asctime)s [%(module)s %(levelname)s] %(message)s'
CELERY_WORKER_TASK_LOG_FORMAT = '%(message)s'
# CELERY_WORKER_LOG_FORMAT = '%(asctime)s [%(module)s %(levelname)s] %(message)s'
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_REDIRECT_STDOUTS = True
CELERY_REDIRECT_STDOUTS_LEVEL = "INFO"
CELERY_WORKER_HIJACK_ROOT_LOGGER = False


# Cache use redis
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://:%(password)s@%(host)s:%(port)s/4' % {
            'password': CONFIG.REDIS_PASSWORD if CONFIG.REDIS_PASSWORD else '',
            'host': CONFIG.REDIS_HOST or '127.0.0.1',
            'port': CONFIG.REDIS_PORT or 6379,
        }
    }
}

# Captcha settings, more see https://django-simple-captcha.readthedocs.io/en/latest/advanced.html
CAPTCHA_IMAGE_SIZE = (80, 33)
CAPTCHA_FOREGROUND_COLOR = '#001100'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
CAPTCHA_TEST_MODE = CONFIG.CAPTCHA_TEST_MODE

COMMAND_STORAGE = {
    'ENGINE': 'terminal.backends.command.db',
}

TERMINAL_COMMAND_STORAGE = {
    "default": {
        "TYPE": "server",
    },
    # 'ali-es': {
    #     'TYPE': 'elasticsearch',
    #     'HOSTS': ['http://elastic:changeme@localhost:9200'],
    # },
}


# Django bootstrap3 setting, more see http://django-bootstrap3.readthedocs.io/en/latest/settings.html
BOOTSTRAP3 = {
    'horizontal_label_class': 'col-md-2',
    # Field class to use in horizontal forms
    'horizontal_field_class': 'col-md-9',
    # Set placeholder attributes to label if no placeholder is provided
    'set_placeholder': True,
    'success_css_class': '',
}

TOKEN_EXPIRATION = CONFIG.TOKEN_EXPIRATION or 3600
DISPLAY_PER_PAGE = CONFIG.DISPLAY_PER_PAGE
DEFAULT_EXPIRED_YEARS = 70
USER_GUIDE_URL = ""
