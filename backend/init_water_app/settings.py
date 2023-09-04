"""
Django settings for init_water_app project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os

from pathlib import Path
import logging.config
import environ
env = environ.Env()
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = os.path.dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = env("DEBUG")

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True


CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:3001',
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'iwater',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'djongo',
    'connection',
    #'django_crontab',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'iwater.middleware.BlockMiddleware',  middlew
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]


ROOT_URLCONF = 'init_water_app.urls'
AUTH_USER_MODEL = "iwater.User"

# CRONJOBS = [
#     ('*/5 * * * *', 'iwater.my_scheduled_job')
# ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'init_water_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DB_NAME = env("DATABASE_NAME")
USER = env("DATABASE_USER")
PASSWORD = env("DATABASE_PASS")
HOST = env("DATABASE_HOST")
PORT = env("DATABASE_PORT")

MONGO_DATABASE_USER=env("MONGO_DATABASE_USER")
MONGO_DATABASE_PASS=env("MONGO_DATABASE_PASS")
MONGO_HOST=env("MONGO_HOST")



DATABASES = {
    'default': {
        'USER': USER, 
        'PASSWORD': PASSWORD,
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
    },
    'default_mongo': {
        'ENGINE': 'djongo',
        'NAME': 'waterinnDB', 
        'CLIENT': {
            'host': MONGO_HOST,   # MongoDB host
            'port': 27017,              # MongoDB port
            'username': MONGO_DATABASE_USER,  # MongoDB username
            'password': MONGO_DATABASE_PASS,  # MongoDB password
            'authSource': 'waterinnDB',      # Authentication source
            'authMechanism': 'SCRAM-SHA-1',  # Authentication mechanism
        },
        'LOGGING': {
                'version': 1,
                'loggers': {
                    'djongo': {
                        'level': 'DEBUG',
                        'propagate': False,                        
                    }
                },
             } 
        
    }
    
}

# SESSION_COOKIE_DOMAIN = "localhost    "


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

# TIME_ZONE = 'UTC'

TIME_ZONE = 'Asia/Kolkata'

# USE_I18N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = '/staticfiles/'
STATIC_URL = 'pub/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# settings.py
# LOGGING_CONFIG=None
DATABASE_ROUTERS = ['connection.router.connectionRouter']

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = (
    # This lets Django's collectstatic store our bundles
    os.path.join(BASE_DIR, 'staticfiles'),
)
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

#EMAIL_PORT = 465      
EMAIL_PORT = 587
#EMAIL_USE_SSL = True
#EMAIL_USE_SSL = False  commented by bharti 
EMAIL_USE_TLS = True

BRAND_NAME = env("BRAND_NAME")
SUPPORT_EMAIL = env("SUPPORT_EMAIL")
SUPPORT_PHONE = env("SUPPORT_PHONE")
# AWS_IOT_ENDPOINT = os.environ.get('AWS_IOT_ENDPOINT')
# CA = os.environ.get('CA')
# CERT = os.environ.get('CERT')
# PRIVATE = os.environ.get('PRIVATE')
AWS_IOT_ENDPOINT = env("AWS_IOT_ENDPOINT")
CA = env("CA")
CERT = env("CERT")
PRIVATE = env("PRIVATE")

AUTH_TOKEN=env("AUTH_TOKEN")
# TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
# TWILIO_DEFAULT_SENDER = env("TWILIO_DEFAULT_SENDER")


# TWILIO_ACCOUNT_SID = "AC7d264f24bf97e9527bda2ccf3aba2af3"       #metric tree commented by bharti
# TWILIO_AUTH_TOKEN = "7ebbd276562397782ee99d10393cfef0"          #metric tree commented by bharti
# TWILIO_DEFAULT_SENDER = "+19714143075"                          #metric tree commented by bharti
 
#TWILIO_ACCOUNT_SID = "AC4b5d2c436341cd60246dbb00e04331e6"        #initiative added by bharti
#TWILIO_AUTH_TOKEN = "c45df71b84ffae11d20ed7cf1e909e98"           #initiatve added by bharti
#TWILIO_DEFAULT_SENDER = "+12763294859"                           #initiative added by bharti

TWILIO_ACCOUNT_SID = "AC7d264f24bf97e9527bda2ccf3aba2af3"       #metric tree commented by bharti
TWILIO_AUTH_TOKEN = "7ebbd276562397782ee99d10393cfef0"          #metric tree commented by bharti
TWILIO_DEFAULT_SENDER = "+19714143075"                          #metric tree commented by bharti




# TWILIO_ACCOUNT_SID = "ACf95045d6cafbe91f7ebdf3caa6100c7c"
# TWILIO_AUTH_TOKEN = "b0b0570763c9b9f14a1b8b0abad84521"
# TWILIO_DEFAULT_SENDER = "+12133194575"
# TWILIO_ACCOUNT_SID = "AC895b46473a36bed46f80344d919f233f"
# TWILIO_AUTH_TOKEN = "b4eb5e22f2740c0427321914ef863413"
# TWILIO_DEFAULT_SENDER = "+19895147363"
# OTP_VALID_FOR = 180  # 180 seconds or 3 minutes
OTP_VALID_FOR = 10  # 180 seconds or 3 minutes
AUTH_LINK_VALID_FOR = 86400

# LOG_FILE_LOCATION = str(BASE_DIR) + env("LOG_FILE_LOCATION")
LOG_FILE_LOCATION = str(BASE_DIR) + "/iwater/log_files/iwater.log"  # TODO
