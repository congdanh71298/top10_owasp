"""
Django settings for top10_owasp project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Get encryption key from environment
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo_app',
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

ROOT_URLCONF = 'top10_owasp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'top10_owasp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'

# Create logs directory path
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Add logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'app.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'todo_app': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Add session security settings
SESSION_COOKIE_AGE = 1800           # Set session timeout to 30 minutes
SESSION_COOKIE_SECURE = True        # Ensures cookies are only sent over HTTPS connections
SESSION_COOKIE_HTTPONLY = True      # Prevents client-side access to cookies via JavaScript

# Security Headers
SECURE_HSTS_SECONDS = 31536000      # Forces HTTPS for 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Applies HSTS to all subdomains
SECURE_HSTS_PRELOAD = True         # Allows site to be included in browser HSTS preload lists
SECURE_REFERRER_POLICY = 'same-origin'  # Only sends referrer header to same origin
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents browser from MIME-sniffing responses
X_FRAME_OPTIONS = 'DENY'            # Prevents site from being embedded in iframes

# Cookie Security
CSRF_COOKIE_SECURE = True           # Ensures CSRF cookies only sent over HTTPS
CSRF_COOKIE_HTTPONLY = True         # Prevents JavaScript access to CSRF cookie
SESSION_COOKIE_SAMESITE = 'Strict'  # Prevents cookie from being sent in cross-site requests
CSRF_COOKIE_SAMESITE = 'Strict'     # Prevents CSRF cookie from being sent in cross-site requests

# Add safety checking config
SAFETY_CHECKS = {
    'ENABLED': True,
    'IGNORE_VULNERABILITIES': [],
    'AUTO_UPDATE': False,
}

# Package management settings
PACKAGE_MANAGERS = {
    'pip': {
        'requirements_file': 'requirements.txt',
        'check_command': 'safety check',
    },
    'npm': {
        'package_file': 'package.json',
        'check_command': 'npm audit',
    }
}
