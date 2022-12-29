# _*_ coding: utf-8 _*_

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置apps路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

DEBUG = os.getenv('DJANGO_DEBUG', default=True)

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', default='t06f*_k9d2!on^#j4k-vw1n5!%mr(+(tn_4)=5jsmt!el9kxg5')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django_celery_results',
	'django_celery_beat',
	'django_filters',
	'rest_framework',
	'guardian',
	'corsheaders',
	'apps.usercenter.apps.UsercenterConfig',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = "apps.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "apps.wsgi.application"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

USE_TZ = True
USE_L10N = True
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"

# session 设置
SESSION_COOKIE_AGE = 60 * 60 * 24  # 一天
SESSION_SAVE_EVERY_REQUEST = True

STATIC_URL = "/static/"
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')

# 自定义用户验证
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    'guardian.backends.ObjectPermissionBackend',
)

# 用户模型设置：
AUTH_USER_MODEL = "usercenter.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPEND_SLASH = True
RUNTIME_DIR = os.path.join(BASE_DIR, 'runtime')
BASE_LOG_DIR = os.path.join(RUNTIME_DIR, "log")

API_VERSION = "api/v1/"

CORS_ORIGIN_WHITELIST = (
	'http://127.0.0.1:8000',
        'http://*',
	'http://localhost:8000',  # 凡是出现在白名单中的域名，都可以访问后端接口
)

LOGIN_REDIRECT_URL='/api/v1/auth/'