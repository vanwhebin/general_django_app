# _*_ coding: utf-8 _*_
# @Time     :   2020/9/14 11:54
# @Author       vanwhebin
import sys
import environ
import os
from datetime import timedelta

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
# 设置apps路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=True)  # 使用.env，此项设置为True

if READ_DOT_ENV_FILE:
	env.read_env(os.path.join(CONFIG_DIR, '.env'))

DEBUG = env.bool('DJANGO_DEBUG', True)

SECRET_KEY = env('DJANGO_SECRET_KEY', default='t06f*_k9d2!on^#j4k-vw1n5!%mr(+(tn_4)=5jsmt!el9kxg5')

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
	'usercenter.apps.UsercenterConfig',
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

ROOT_URLCONF = 'workApp.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
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

WSGI_APPLICATION = 'workApp.wsgi.application'

# 项目用户验证模型
AUTH_USER_MODEL = "usercenter.User"

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'guardian.backends.ObjectPermissionBackend',
)

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

LANGUAGE_CODE = 'zh-Hans'

# TIME_ZONE = 'Asia/Shanghai'
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': env('MYSQL_DATABASE', default='django-bi'),
		'HOST': env('MYSQL_HOST', default='192.168.56.103'),
		'PORT': env('MYSQL_PORT', default='3306'),
		'USER': env('MYSQL_USER', default='root'),
		'PASSWORD': env('MYSQL_PASSWORD', default='root'),
		'OPTIONS': {'charset': 'utf8mb4'}
	}
}

CACHES = {
	"default": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": "redis://127.0.0.1:6379/1",
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
		},
		"TIMEOUT": 3600
	}
}

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
UPLOAD_MEDIA_CHOICES = (
	(".pdf", "PDF"), (".xlsx", "EXCEL"), (".xls", "EXCEL"), (".doc", "DOC"), (".docx", "DOC"),
	(".ppt", "PPT"), (".png", "IMAGE"), (".jpg", "IMAGE"),
)

# 配置celery时区，默认时UTC。
if USE_TZ:
	CELERY_TIMEZONE = TIME_ZONE

# celery异步设置
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/15'  # Broker配置，使用Redis作为消息中间件
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # BACKEND配置，使用redis
CELERY_RESULT_BACKEND = 'django-db'  # 使用django orm 作为结果存储
CELERY_RESULT_SERIALIZER = 'json'  # 结果序列化方案
DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191
CELERY_TASK_SERIALIZER = 'json'  # 序列化方式  默认是json
CELERY_ACCEPT_CONTENT = ['json']  # 结果格式  默认也是json
CELERY_CONCURRENCY = 4  # celery worker并发数
CELERY_MAX_TASKS_PER_CHILD = 4  # 每个worker最大执行任务数

DJANGO_CELERY_BEAT_TZ_AWARE = True
CELERY_ENABLE_UTC = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'  # 定時任务调度器
C_FORCE_ROOT = True

CORS_ORIGIN_WHITELIST = (
	'http://127.0.0.1:8000',
        'http://*',
	'http://localhost:8000',  # 凡是出现在白名单中的域名，都可以访问后端接口
)


APPEND_SLASH = True
RUNTIME_DIR = os.path.join(BASE_DIR, 'runtime')
BASE_LOG_DIR = os.path.join(RUNTIME_DIR, "log")

REST_FRAMEWORK = {
	# Use Django's standard `django.contrib.auth` permissions,
	# or allow read-only access for unauthenticated users.
	'DEFAULT_PERMISSION_CLASSES': [
		# 'rest_framework.permissions.IsAuthenticated',
		# 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
		# 'rest_framework.permissions.Is',
		'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
	],
	'DEFAULT_AUTHENTICATION_CLASSES': [
		# 'rest_framework.authentication.TokenAuthentication',
		'rest_framework_simplejwt.authentication.JWTAuthentication',
		'rest_framework.authentication.SessionAuthentication',
	],
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
		'rest_framework.renderers.BrowsableAPIRenderer',
		# 'rest_framework_csv.renderers.CSVRenderer',
	),

}

SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
	'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
	'SIGNING_KEY': '4ZSsKxb$NWV&V1rd*KS6yJROOh!!!HB3&W!jUTyBc9iOLptwzW*g^3GG*ZDdtJT1',
	'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
	'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_EXPIRE = 3600 * 2
REDIS_DB = 1
REDIS_PREFIX = 'workApp_'


SYS_ACCOUNTS = {
	"BY": {
		"username": "wanweibin@aukeys.com",
		"password": '123456',
	},
	"BI": {
		"username": "wanweibin@aukeys.com",
		"password": '999@wanweibin',
	},
	"YY": {
		"username": "dubo@aukeys.com",
		"password": 'aukey@123'
	}
}


EMAIL_HOST = "smtp.exmail.qq.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = "wanweibin@aukeys.com"
EMAIL_HOST_PASSWORD = "69#fnnGApa&t"
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = 60

EMAIL_TO = "tanbo@aukeys.com"

API_VERSION = "api/v1/"
