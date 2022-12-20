# _*_ coding: utf-8 _*_
# @Time     :   2020/10/13 12:27
# @Author       vanwhebin

import redis

from workApp import settings


class RedisClient:
	instance = None

	def __init__(self):
		if self.instance is None:
			self.instance = redis.Redis(
				host=settings.REDIS_HOST,
				port=settings.REDIS_PORT,
				db=settings.REDIS_DB,
				decode_responses=True
			)

	def set_item(self, key, value, expire=None):
		if not isinstance(key, str):
			raise TypeError(u"键值类型必须为字符串")
		ex = expire if expire else settings.REDIS_EXPIRE
		prefix_key = settings.REDIS_PREFIX + key
		return self.instance.set(prefix_key, value, ex)

	def get_item(self, key):
		return self.instance.get(key)
