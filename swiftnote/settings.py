import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables from .env file (for local development)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-xxxxxx')  # Secure your secret key in environment variables
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'swiftnoteapp.onrender.com']  # Add your Render app URL here

CSRF_TRUSTED_ORIGINS = [
    'https://swiftnoteapp.onrender.com',
    # Add more domains if necessary
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notes',
    'tasks',
    'django_celery_beat',
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

ROOT_URLCONF = 'swiftnote.urls'

# Email settings (for sending emails)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development, replace with actual backend in production
EMAIL_HOST = 'smtp.gmail.com'  # Replace with your email provider's host
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'mwendeclemence@gmail.com')  # Use environment variable
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'your-email-password')  # Use environment variable

# Celery configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')  # Use Redis URL for local dev or Render production
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')  # Use Redis URL for local dev or Render production
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERY_TASK_RESULT_EXPIRES = 3600


# Optional: Configure periodic tasks using Celery Beat
CELERY_BEAT_SCHEDULE = {
    'send-task-reminders': {
        'task': 'tasks.tasks.send_task_reminder',
        'schedule': 60.0,  # Every minute (for example)
    },
}

# Login URL and Redirect
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Custom User Model
AUTH_USER_MODEL = 'notes.CustomUser'

# Static Files Configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'notes', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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

WSGI_APPLICATION = 'swiftnote.wsgi.application'

import os
from urllib.parse import urlparse

# Get the DATABASE_URL environment variable for production (Render)
DATABASE_URL = os.getenv('DATABASE_URL')

# Check if we're in local development (MySQL) or production (PostgreSQL)
if DATABASE_URL:
    # If DATABASE_URL exists, we're in production (Render, using PostgreSQL)
    url = urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',  # PostgreSQL for Render
            'NAME': url.path[1:],  # Database name (after the first '/')
            'USER': url.username,  # Username
            'PASSWORD': url.password,  # Password
            'HOST': url.hostname,  # Hostname (the address of the database)
            'PORT': url.port,  # Port (5432 is default for PostgreSQL)
        }
    }
else:
    # If DATABASE_URL does not exist, use MySQL for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
