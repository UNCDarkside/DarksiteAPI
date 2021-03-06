"""
Django settings for darksite project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

if not SECRET_KEY and DEBUG:
    SECRET_KEY = "debug"

# Two cases to handle:
# 1. If values are provided, we should parse the comma-separated list.
# 2. If no value is provided, the result should be an empty list rather
#    than a list with an empty string.
ALLOWED_HOSTS = [
    host for host in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if host
]


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = ["adminsortable2", "corsheaders", "graphene_django"]

CUSTOM_APPS = ["account", "cms", "cms.blog", "teams"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "darksite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "darksite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# We assume that the provided credentials are for a Postgres DB. If the
# appropriate credentials are not provided, we fall back to the local
# sqlite DB.

DB_HOST = os.getenv("DJANGO_DB_HOST", "localhost")
DB_NAME = os.getenv("DJANGO_DB_NAME")
DB_PASSWORD = os.getenv("DJANGO_DB_PASSWORD")
DB_PORT = os.getenv("DJANGO_DB_PORT", "5432")
DB_USER = os.getenv("DJANGO_DB_USER")

if all((DB_HOST, DB_USER, DB_PASSWORD, DB_PORT)):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }


# Custom User Model

AUTH_USER_MODEL = "account.User"


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"  # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Media Files (User Uploaded)

MEDIA_ROOT = os.getenv("DJANGO_MEDIA_ROOT")
MEDIA_URL = "/media/"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.getenv("DJANGO_STATIC_ROOT")
STATIC_URL = "/static/"


# File Storage

if os.getenv("DJANGO_SPACES_STORAGE", "False").lower() == "true":
    DEFAULT_FILE_STORAGE = "custom_storages.backends.MediaStorage"
    STATICFILES_STORAGE = "custom_storages.backends.StaticStorage"

    AWS_ACCESS_KEY_ID = os.getenv("DJANGO_SPACES_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.getenv("DJANGO_SPACES_SECRET_KEY")

    AWS_S3_REGION_NAME = os.getenv("DJANGO_SPACES_REGION")
    AWS_S3_ENDPOINT_URL = (
        f"https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com"
    )
    AWS_STORAGE_BUCKET_NAME = os.getenv("DJANGO_SPACES_BUCKET")

    AWS_S3_CUSTOM_DOMAIN = os.getenv("DJANGO_SPACES_DOMAIN")
    STATIC_URL = f"{AWS_S3_CUSTOM_DOMAIN}/"
    MEDIA_URL = f"{AWS_S3_CUSTOM_DOMAIN}/"


# Allow for in-memory file storage

if os.getenv("DJANGO_IN_MEMORY_FILES", "False").lower() == "true":
    DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"


# CORS - The API should be accessible from anywhere

CORS_ORIGIN_ALLOW_ALL = True


# Graphene Django

GRAPHENE = {"SCHEMA": "darksite.schema.schema"}


# Logging Configuration

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "[%(asctime)s] %(levelname)8s [%(name)s:%(lineno)s] %(message)s",  # noqa
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "standard"},
        "null": {"class": "logging.NullHandler", "level": "DEBUG"},
    },
    "loggers": {
        # Root Handler
        "": {"handlers": ["console"], "level": "WARNING"},
        # Customized Handlers
        "django.request": {"level": "ERROR", "propagate": True},
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}

# We want more logging for our custom apps
for app in CUSTOM_APPS:
    LOGGING["loggers"][app] = {
        "handlers": ["console"],
        "level": "INFO",
        "propagate": False,
    }
