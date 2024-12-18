import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables from .env file (for local development)
load_dotenv()

# Get SECRET_KEY from environment variable. In development, you can have a fallback, but not in production.
SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY:
    if DEBUG:  # Fallback for local development
        SECRET_KEY = 'django-insecure-xxxxxx'  # Temporary fallback key for local development
    else:
        raise ValueError("No SECRET_KEY set in the environment variables. Please set it for production.")

# Get DEBUG from environment variables. It defaults to False if not set.
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Load environment variables from .env file (for local development)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

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

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise storage for compressed static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (optional)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


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



# Load ALLOWED_HOSTS from environment variable and convert it into a list
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost,swiftnoteapp.onrender.com')

# Convert the comma-separated string to a list
ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')

# Load CSRF_TRUSTED_ORIGINS from environment variable and convert it into a list
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://swiftnoteapp.onrender.com,https://localhost:8000')

# Convert the comma-separated string to a list
CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGINS.split(',')

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Use PostgreSQL for production
    url = urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        }
    }
else:
    # Use MySQL for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'default_db_name'),
            'USER': os.getenv('DB_USER', 'default_db_user'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'default_db_password'),
            'HOST': os.getenv('DB_HOST', '127.0.0.1'),
            'PORT': os.getenv('DB_PORT', '3306'),
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
