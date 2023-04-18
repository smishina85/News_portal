"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from dotenv import load_dotenv
from pathlib import Path
#import warnings

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dv_u)gz%#ens!sj#9k^0*@s8l(c#qze78k(y#p4vs2xozv%a-x'

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
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django.contrib.flatpages',
    'news',
    'django_filters',
    'accounts',
    'django_apscheduler',
    'django_celery_beat',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

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

# Этого раздела может не быть, добавьте его в указанном виде for allauth.
AUTHENTICATION_BACKENDS = [
    #встроенный бэкенд Django — 'django.contrib.auth.backends.ModelBackend' — реализующий аутентификацию по username;
    'django.contrib.auth.backends.ModelBackend',
    #бэкенд аутентификации, предоставленный пакетом allauth — 'allauth.account.auth_backends.AuthenticationBackend'.
    'allauth.account.auth_backends.AuthenticationBackend',
]




WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [BASE_DIR / "static"]

LOGIN_REDIRECT_URL = "/allnews"
LOGOUT_REDIRECT_URL = '/allnews'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
#ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}
ACCOUNT_CONFIRM_EMAIL_ON_GET = True  #позволит избежать дополнительного входа и активирует аккаунт сразу, как только мы перейдём по ссылке
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 4  #хранит количество дней, когда доступна ссылка на подтверждение регистрации

# warnings.filterwarnings(
#     'error', r"DateTimeField .* received a naive datetime",
#     RuntimeWarning, r'django\.db\.models\.fields',
# )

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' #класс отправителя сообщений (у нас установлено значение по умолчанию, а значит, эта строчка не обязательна);
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru' #хост почтового сервера
EMAIL_PORT = 465 #порт, на который почтовый сервер принимает письма
EMAIL_HOST_USER = 'kind.mishina' #логин пользователя почтового сервера
#EMAIL_HOST_PASSWORD = "________" #пароль пользователя почтового сервера
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') #пароль пользователя почтового сервера
EMAIL_USE_TLS = False #необходимость использования TLS (зависит от почтового сервера, смотрите документацию по настройке работы с сервером по SMTP)
EMAIL_USE_SSL = True #необходимость использования SSL (зависит от почтового сервера, смотрите документацию по настройке работы с сервером по SMTP);

#DEFAULT_FROM_EMAIL = '______' #почтовый адрес отправителя по умолчанию.
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL') #почтовый адрес отправителя по умолчанию.

SERVER_EMAIL = 'kind.mishina@yandex.ru'
MANAGERS = (
    ('Svetlana', 'kind.mishina@yandex.ru'),
)
ADMINS = (
    ('admin', 'snys@mac.com'),
)

EMAIL_SUBJECT_PREFIX = 'Наш портал '

CELERY_BROKER_URL = 'redis://localhost:6379'  # указывает на URL брокера сообщений (Redis). По умолчанию он находится на порту 6379.
CELERY_RESULT_BACKEND = 'redis://localhost:6379'  #указывает на хранилище результатов выполнения задач
CELERY_ACCEPT_CONTENT = ['application/json']  # допустимый формат данных
CELERY_TASK_SERIALIZER = 'json'  # метод сериализации задач.
CELERY_RESULT_SERIALIZER = 'json' # метод сериализации результатов.
CELERY_IMPORTS = ('news.tasks',)
CELERY_TIMEZONE = 'Europe/Moscow'
#CELERY_TASK_TIME_LIMIT = 30 * 60
# время жизни таски

# Если вы используете Redis Labs, то переменные CELERY_BROKER_URL и CELERY_RESULT_BACKEND должны строиться по шаблону:
#
# redis://логин:пароль@endpoint:port
# где endpoint и port вы также берёте из настроек Redis Labs.

# Также обратите внимание, что Celery с версией выше 4+ не поддерживается Windows.
# Поэтому если у вас версия Python 3.10 и выше, запускайте Celery, добавив в команду флаг: --pool=solo.

