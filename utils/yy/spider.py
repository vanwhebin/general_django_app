# _*_ coding: utf-8 _*_
# @Time     :   2020/10/20 17:34
# @Author       vanwhebin
import time
import json
import copy
import re
import random

import requests

from workApp.settings import SYS_ACCOUNTS
from utils.util import get_yesterday, save_log


class DataSpider:
	""" 鹰眼系统的数据爬取"""
	log = 'yy'
	login_dict = {
		"email": SYS_ACCOUNTS['YY']['username'],
		"password": SYS_ACCOUNTS['YY']['password']
	}

	site_url = "http://a.aukeyit.com/"

	auth_prefix = "OPS "

	urls = {
		"login": {"url": "DOMAIN/auth/api/v1/api-token-auth/", "method": "POST", 'ajax': True},
		"create": {"url": "DOMAIN/report/api/v1/analysis_report/", "method": "POST", 'ajax': True},
		"result": {"url": "DOMAIN/report/api/v1/analysis_report_watch/", "method": "POST", 'ajax': True},

	}

	headers = {
		'X-Requested-With': 'XMLHttpRequest',
		'Referer': 'DOMAIN/front/analysis/marketshare',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
		'Cookie': ""
	}

	survey_params = {
		"category": None,
		"category_url": None,
		"type": None,
		"brand": "",
		"brand_t": "",
		"brand_tmp": [],
		"remark": "",
		"password": None
	}

	def __init__(self, **kwargs):
		self.s = requests.session()
		self.login()

	def request(self, url_index, headers=None, data=None, params=None):
		# 封装requests库在当前类的使用
		# cookie 使用字符串加上分号结尾
		url_dict = copy.deepcopy(self.urls[url_index])
		url_dict['url'] = re.sub(r"DOMAIN", self.site_url, self.urls[url_index]['url'])

		_d = []
		if "ipCheck" in self.s.cookies:
			_d.append(f"ipCheck={self.s.cookies['ipCheck']}")
		if "tokenRegTime" in self.s.cookies:
			_d.append(f"tokenRegTime={self.s.cookies['tokenRegTime']}")
		if "token" in self.s.cookies:
			_d.append(f"token={self.s.cookies['token']}")
			self.headers['Authorization'] = self.auth_prefix + str(self.s.cookies['token'])
		if "user" in self.s.cookies:
			_d.append(f"user={self.s.cookies['user']}")
		if "loginWay" in self.s.cookies:
			_d.append(f"loginWay={self.s.cookies['loginWay']}")
		self.headers['Cookie'] = ";".join(_d)
		request_headers = self.headers
		request_headers['Referer'] = self.site_url + self.urls['login']['url']
		response = None
		request_data = data if data else {}
		request_headers = {**request_headers, **headers} if headers else request_headers

		request_start = time.strftime("%Y-%m-%d %H:%M:%S")

		if url_dict['method'] == "POST":
			response = self.s.post(url_dict['url'], data=request_data, headers=request_headers, params=params)
		elif url_dict['method'] == "GET":
			response = self.s.get(url_dict['url'], headers=request_headers, params=params)

		log = {
			"start_time": request_start,
			"请求头": str(request_headers),
			"请求参数: ": {"params": params, "data": request_data},
			"cookies: ": str(self._get_request_cookies()),
			"返回cookies: ": str(requests.utils.dict_from_cookiejar(response.cookies)),
			"请求方式": str(url_dict),
			"请求响应: ": str(response.status_code),
			"请求返回头部": str(response.headers),
			"end_time": time.strftime("%Y-%m-%d %H:%M:%S"),
		}

		self.save_log(log)
		return response

	def _get_request_cookies(self):
		""" 获取request请求会话中的cookie """
		cookies = requests.utils.dict_from_cookiejar(self.s.cookies)
		return cookies

	def login(self):
		login_dict = copy.deepcopy(self.login_dict)
		login_res = self.request('login', data=login_dict)
		if login_res.status_code == 200:
			print(u"登录成功")
			return True
		else:
			print(u"登录失败")
			raise RuntimeError(u"登录失败")

	def save_log(self, content):
		""" 将爬取数据写入日志文件 """
		save_log(self.log, content, 'spider')

	@staticmethod
	def _create_pwd():
		""" 创建对应的报告的获取密码 """
		return hex(random.randint(11111111, 99999999))

	def create_survey(self, **kwargs):
		""" 创建调研报告 """
		params_type = ("market_research", "brand_research")
		if ("category" not in kwargs) or ("category_url" not in kwargs) \
			or ("type" not in kwargs) or (kwargs["type"] not in params_type):
			raise KeyError(u"获取调研报告参数错误")

		code = self._create_pwd()
		create_params = {**self.survey_params, **{
			"category": kwargs['category'],
			"category_url": kwargs['category_url'],
			"type": kwargs['type'],
			"password": code[2:8]
			}
		}

		res = self.request("create", data=create_params)
		if res.status_code == 201:
			return {"params": create_params, "data": json.loads(res.content), "password": code[2:8]}
		else:
			raise RuntimeError(u"创建新调研项目失败")

	def get_survey_result(self, **kwargs):
		""" 获取调研报告 内容"""
		if ("url_code" not in kwargs) or ("password" not in kwargs):
			raise KeyError(u"获取调研报告参数错误")
		result_params = {
			"url_code": kwargs['url_code'],
			"password": kwargs['password']
		}
		res = self.request("result", data=result_params)
		if res.status_code == 200:
			return json.loads(res.content)
		else:
			raise RuntimeError(u"创建新调研项目失败")


