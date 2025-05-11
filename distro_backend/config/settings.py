import os
from pathlib import Path
from datetime import timedelta
from environ import Env

env = Env()
Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('DJANGO_SECRET_KEY', default='your-secret-key-here')
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'backend',
    'bomet.localhost',
    'turkana.localhost',
    '*.distro.africa',
]

SHARED_APPS = [
    'django_tenants',
    'tenants',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'distro',
]

TENANT_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'prometheus_client',
    'leaflet',
    'django_ckeditor_5',
    'distro',
]

INSTALLED_APPS = SHARED_APPS + [app for app in TENANT_APPS if app not in SHARED_APPS]

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'distro.middleware.TenantHeaderMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'distro',
        'USER': 'distro',
        'PASSWORD': '123456789',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ORIGINAL_BACKEND = 'django.contrib.gis.db.backends.postgis'

TENANT_MODEL = 'tenants.Tenant'
TENANT_DOMAIN_MODEL = 'tenants.Domain'
PUBLIC_SCHEMA_NAME = 'public'
PUBLIC_SCHEMA_URLCONF = 'config.urls'
DATABASE_ROUTERS = ['django_tenants.routers.TenantSyncRouter']
POSTGIS_VERSION = (3, 3, 0)

# Tenant-specific settings
SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
TENANT_AUTO_CREATE_SCHEMA = True
TENANT_SUBFOLDER_PATH = None

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise configuration
# Use the default storage backend that works with WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# WhiteNoise settings for django-tenants compatibility
WHITENOISE_USE_FINDERS = True  # Search static files in STATICFILES_DIRS
WHITENOISE_AUTOREFRESH = DEBUG  # Auto-refresh in debug mode

# Optional: Configure static file caching
if not DEBUG:
    WHITENOISE_MAX_AGE = 31536000  # 1 year cache for static files

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

AUTH_USER_MODEL = 'distro.UserProfile'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://frontend:3000',
    'http://bomet.localhost:80',
    'http://turkana.localhost:80',
    'http://localhost:80',
]
CORS_ALLOW_CREDENTIALS = True

DJANGO_CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote'],
        'height': 300,
        'width': '100%',
    },
}

PROMETHEUS_EXPORT_MIGRATIONS = False