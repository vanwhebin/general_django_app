from workApp.settings import USE_TZ, TIME_ZONE

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
