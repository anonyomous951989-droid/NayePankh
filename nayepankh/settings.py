"""
==============================================================
NayePankh Foundation - Volunteer Registration System
Django Settings Configuration
==============================================================
This file contains all the configuration for the Django project.
For beginners: Settings control how Django behaves. Each setting
is documented with comments explaining its purpose.
==============================================================
"""

import os
from pathlib import Path
from decouple import config,Csv

# ==============================================================
# BASE DIRECTORY
# ==============================================================
# Build paths inside the project like this: BASE_DIR / 'subdir'
# BASE_DIR points to the root folder of the project (where manage.py is)
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================
# SECURITY SETTINGS
# ==============================================================
# SECURITY WARNING: keep the secret key used in production secret!
# The SECRET_KEY is used for cryptographic signing (sessions, tokens, etc.)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-me-in-production-12345')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG=True shows detailed error pages. Set to False in production.
DEBUG = config('DEBUG', default=True, cast=bool)

# List of host/domain names that this Django site can serve
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ==============================================================
# APPLICATION DEFINITION
# ==============================================================
# Django apps are modular components. We register both built-in
# and our custom apps here.
INSTALLED_APPS = [
    # --- Django Built-in Apps ---
    'django.contrib.admin',           # Admin panel
    'django.contrib.auth',            # Authentication framework
    'django.contrib.contenttypes',    # Content type framework
    'django.contrib.sessions',        # Session framework
    'django.contrib.messages',        # Messaging framework
    'django.contrib.staticfiles',     # Static file management
    'django.contrib.humanize',        # Template filters for human-readable data

    # --- Third-Party Apps ---
    'rest_framework',                 # Django REST Framework for API
    'django_filters',                 # Filtering support

    # --- Our Custom Apps ---
    'accounts.apps.AccountsConfig',       # User authentication & management
    'volunteers.apps.VolunteersConfig',   # Volunteer registration & profiles
    'events.apps.EventsConfig',           # Event management
    'dashboard.apps.DashboardConfig',     # Volunteer & admin dashboards
    'reports.apps.ReportsConfig',         # Reports & data export
    'core.apps.CoreConfig',               # Landing page & contact
    'api.apps.ApiConfig',                 # REST API endpoints
]

# ==============================================================
# MIDDLEWARE
# ==============================================================
# Middleware processes requests/responses globally before they
# reach views or after views return responses.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session support
    'django.middleware.common.CommonMiddleware',             # Common utilities
    'django.middleware.csrf.CsrfViewMiddleware',            # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Auth support
    'django.contrib.messages.middleware.MessageMiddleware',  # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# ==============================================================
# URL CONFIGURATION
# ==============================================================
# Points to the root URL configuration module
ROOT_URLCONF = 'nayepankh.urls'

# ==============================================================
# TEMPLATE CONFIGURATION
# ==============================================================
# Configure Django's template engine (how HTML files are rendered)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Look for templates in these directories first
        'DIRS': [BASE_DIR / 'templates'],
        # Also look inside each app's 'templates/' folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',    # Makes 'request' available in templates
                'django.contrib.auth.context_processors.auth',   # Makes 'user' available in templates
                'django.contrib.messages.context_processors.messages',  # Makes 'messages' available
            ],
        },
    },
]

# ==============================================================
# WSGI APPLICATION
# ==============================================================
WSGI_APPLICATION = 'nayepankh.wsgi.application'

# ==============================================================
# DATABASE CONFIGURATION
# ==============================================================
# Using PostgreSQL as our database
# For beginners: A database stores all your app's data (users, volunteers, events, etc.)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='nayepankh_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

# ==============================================================
# AUTHENTICATION
# ==============================================================
# Tell Django to use our custom User model instead of the default one
AUTH_USER_MODEL = 'accounts.User'

# Where to redirect after login/logout
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ==============================================================
# PASSWORD VALIDATION
# ==============================================================
# These validators ensure users create strong passwords
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================
# INTERNATIONALIZATION
# ==============================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'    # Indian Standard Time
USE_I18N = True
USE_TZ = True

# ==============================================================
# STATIC FILES (CSS, JavaScript, Images)
# ==============================================================
# URL prefix for static files
STATIC_URL = '/static/'

# Additional directories where Django looks for static files
STATICFILES_DIRS = [BASE_DIR / 'static']

# Directory where collectstatic will copy all static files (for production)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ==============================================================
# MEDIA FILES (User-uploaded files: resumes, photos, etc.)
# ==============================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================================================
# EMAIL CONFIGURATION (Gmail SMTP)
# ==============================================================
# For development, use console backend to see emails in terminal:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production, use Gmail SMTP:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='anonyomous951989@gmail.com')

# ==============================================================
# DJANGO REST FRAMEWORK CONFIGURATION
# ==============================================================
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# ==============================================================
# FILE UPLOAD SETTINGS
# ==============================================================
# Maximum upload size: 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024   # 5 MB

# ==============================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
