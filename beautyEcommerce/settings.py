"""
Django settings for beautyEcommerce project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the SECRET_KEY from the environment variable
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# Raise an error if the SECRET_KEY is not set
if not SECRET_KEY:
    raise ValueError("The DJANGO_SECRET_KEY environment variable is not set!")

#SECRET_KEY = 'django-insecure-v2_6(yenff3ay#av3zx%!9vc=2^-ynu%av^9hz10(iv5bq)5si'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['lyraqueenbeautyproduct.onrender.com', 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = [
    'https://lyraqueenbeautyproduct.onrender.com',  # Add your domain here
    'https://your-other-trusted-domain.com',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'productApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'beautyEcommerce.urls'

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

WSGI_APPLICATION = 'beautyEcommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lyraqueen',
        'USER': 'lyraqueen_user',
        'PASSWORD': 'AX7uKa7OPX4keCKC0BOvQX49YqBcJkHX',
        'HOST': 'dpg-ctskoibtq21c739atgcg-a.singapore-postgres.render.com',
        'PORT': '5432',
    }
}


'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'product',
        'USER': 'postgres',
        'PASSWORD': 'postgres123',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}'''


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
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "productApp" / "static",  # Correct path to the static directory
]

STATIC_ROOT = BASE_DIR/'beautyfiles'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Make sure you have this enabled
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # or choose another backend if needed
SESSION_COOKIE_NAME = 'sessionid'  # Ensure session cookie is named properly
SESSION_COOKIE_AGE = 60*60*24 # Set the session to expire after 24hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Ensure the session expires when the browser is closed

#payment gateway integration

RAZORPAY_KEY_ID = 'rzp_test_MCNdX8AKxvoM4b'
RAZORPAY_KEY_SECRET = 'rVnrk2mT7ZVAtbONgfU2LMfQ'

CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
