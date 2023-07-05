

from pathlib import Path

# Enviroment variables
import environ
env = environ.Env()
environ.Env.read_env()

NUM_OF_CONVERSATIONS_PER_SURVEY = env.int('NUM_OF_CONVERSATIONS_PER_SURVEY')
BASIC_AUTH_USERNAME = env.str('BASIC_AUTH_USERNAME')
BASIC_AUTH_PASSWORD = env.str('BASIC_AUTH_PASSWORD')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Paths
import os
CONVERSATIONS_DIR = os.path.join(BASE_DIR, r'surveyapp\data\conversations')
CONVERSATIONS_PATH = os.path.join(BASE_DIR, r'surveyapp\data\all_conversations.xlsx')
USERS_PATH = os.path.join(BASE_DIR, r'surveyapp\data\all_users.xlsx')
USERS_SURVEYS_DIR = os.path.join(BASE_DIR, r'surveyapp\data\users_surveys')

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'survey',
    'user'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'surveyapp.urls'

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


WSGI_APPLICATION = 'surveyapp.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

