"""
Django settings for gesinfraweb project.
"""

from pathlib import Path
import os  # Importación necesaria para las rutas

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-myw@hddj_g&0(4mo5rxg1y46yuz9%5-+gubarzfn1@so#@0z#w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Mis aplicaciones
    'registro_calificaciones',
    'inventario_equipos',
    'accesibilidad',
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

ROOT_URLCONF = 'gesinfraweb.urls'

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

WSGI_APPLICATION = 'gesinfraweb.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- CONFIGURACIÓN DE FORMATO DE FECHA (SOLUCIÓN AL ERROR) ---
# Esto le dice a Django que acepte el formato día/mes/año
DATE_INPUT_FORMATS = [
    '%d/%m/%Y',  # Acepta: 27/01/2026
    '%d-%m-%Y',  # Acepta: 27-01-2026
    '%Y-%m-%d',  # Acepta: 2026-01-27 (Estándar)
]
# -------------------------------------------------------------

# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS ---

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# --------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirecciones de Login/Logout
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'