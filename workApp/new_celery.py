# _*_ coding: utf-8 _*_
# @Time     :   2020/8/31 20:17
# @Author       vanwhebin


# from __future__ import absolute_import, unicode_literals
import os
# from django.utils import timezone
from celery import Celery
from django.apps import apps, AppConfig

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workApp.settings')

app = Celery('workApp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
task_dir = ['tasksapp', ]


# app.autodiscover_tasks(packages=task_dir, force=True)
app.autodiscover_tasks()


# class CeleryAppConfig(AppConfig):
# 	name = 'tasks'
# 	verbose_name = 'Celery Config'
#
# 	def ready(self):
# 		installed_apps = [app_config.name for app_config in apps.get_app_configs()]
# 		app.autodiscover_tasks(lambda: installed_apps, force=True)
		# app.autodiscover_tasks(task_dir, force=True)


# 解决时区问题,定时任务启动就循环输出
# app.now = timezone.now
# 用于测试的异步任务
@app.task(bind=True)
def debug_task(self):
	return 'Request: {0!r}'.format(self.request)
