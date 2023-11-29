# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config
from unipath import Path
import dj_database_url
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import blog

BASE_DIR = Path(__file__).parent
# print(BASE_DIR)
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(CORE_DIR)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# load production server from .env
# Application definition

INSTALLED_APPS = [
    # 'seo',
    # 'modeltranslation',  # optional
    # 'django_jinja',  # optional for jinja2 global function
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'debug_toolbar',
    "crispy_forms",
    "django_summernote",
    'website',
    'bootstrap4',
    'decom',  # 反编译
    'blog',  #
]

TRANSLATABLE_MODEL_MODULES = ["blog.models"]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # 新增多语支持
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'website.urls'

LOGIN_REDIRECT_URL = "home"  # Route defined in decom/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in decom/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "website/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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
SITE_ID = 1

WSGI_APPLICATION = 'website.wsgi.application'
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join("db/", 'anytools'),
        # 'NAME': 'cms',
        # 'USER': 'cms',
        # 'PASSWORD': '1qaz@WSX',
        # 'HOST': '127.0.0.1',
        # 'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('zh-hans', _('Simplified Chinese')),
)
PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))
LOCALE_PATHS = (os.path.join(PROJECT_ROOT, 'locale'),)
#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static decompiler (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# # STATICFILES_DIRS = [ os.path.join(CORE_DIR, "../static/"),]
# STATICFILES_DIRS = [ "/Users/qianli/workspace/python/www/static"]
# # STATIC_URL = '/static/'
# STATIC_URL = '/Users/qianli/workspace/python/www/static'
# # STATIC_ROOT = os.path.join(CORE_DIR, "static")
# STATIC_ROOT = "/Users/qianli/workspace/python/www/static_web";


CRISPY_TEMPLATE_PACK = "bootstrap4"
# Media paths

# Base url to serve media files
MEDIA_URL = "/media/"

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
X_FRAME_OPTIONS = "SAMEORIGIN"

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
################################################

LOGGING = {
    'version': 1,  # 版本
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 过滤器
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',  # 输出等级为“INFO”
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',  # 输出等级为“INFO”
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "../logs/msg.log",  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,  # 日志文件的大小（300*1024*1024为300MB）
            'backupCount': 10,  # 日志文件的数量（超过设定的最大值会自动备份，备份数量最大值为10）
            'formatter': 'verbose'  # 日志输出格式：使用了在之前定义的'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
