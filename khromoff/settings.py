import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv("SECRET_KEY", default="default secret key (woo!)")
STAFF_TG_ID = os.getenv("STAFF_TG_ID")

DEBUG = True
DOMAIN_NAME = 'khrmff.test'
if not os.environ.get("IS_DEBUG"):
    DEBUG = False
    DOMAIN_NAME = 'khrmff.ru'
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    # SECURE_SSL_REDIRECT = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'

ALLOWED_HOSTS = ['*']
LOGIN_URL = '//%s/login' % DOMAIN_NAME

SESSION_COOKIE_DOMAIN = DOMAIN_NAME

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} - {asctime} | {module}: {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'infile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'verbose'
        },
        'telegram_log': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'bughunter.apps.TelegramLogHandler',
            'bot_token': os.getenv("TELEGRAM_BOT_TOKEN"),
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'infile'],
        },
        'django.request': {
            'handlers': ['telegram_log'],
            'level': 'ERROR',
        },
        'khromoff': {
            'handlers': ['console', 'infile'],
            'level': 'DEBUG',
            'formatters': ['verbose']
        },
        'khromoff.bugs': {
            'handlers': ['telegram_log'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'urlshortner.apps.UrlshortnerConfig',
    'api.apps.ApiConfig',
    'bughunter.apps.BughunterConfig',
    'blog.apps.BlogConfig',

    # 3rd party
    'rest_framework',
    'django_log_to_telegram',
    'rest_framework_api_key',
    'django_hosts',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'khromoff.urls'

ROOT_HOSTCONF = 'khromoff.hosts'
DEFAULT_HOST = 'index'
PARENT_HOST = DOMAIN_NAME

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/'),
            os.path.join(BASE_DIR, 'khromoff/templates/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # my processors
                'khromoff.context_processor.static_context',
                'khromoff.context_processor.debug',
                'khromoff.context_processor.is_subdomain',

                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django_hosts.templatetags.hosts_override'
            ]
        },
    },
]

WSGI_APPLICATION = 'khromoff.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
        'PASSWORD': 'postgres',
        'USER': 'postgres'
    }
}

if DEBUG:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.mysqlite3',
    }

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'api.utils.APITokenAuth',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'api.utils.UserAPIKeyThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '15/min',
        'user': '30/min',
    },

    'EXCEPTION_HANDLER': 'api.handlers.api_exception_handler',
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = False

USE_TZ = True

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "general_static"),
    os.path.join(BASE_DIR, "khromoff/static/")
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
