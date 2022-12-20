# _*_ coding: utf-8 _*_
# @Time     :   2020/8/27 15:34
# @Author       vanwhebin
import json
import os
import copy
import datetime
import re
import time

import requests

from workApp.settings import SYS_ACCOUNTS
from utils.by.aes_encrypt import Encrypt
from utils.util import save_log
from workApp.settings import BASE_LOG_DIR


class DataSpider:
	log = 'by'
	login_dict = {
		"username": SYS_ACCOUNTS['BY']['username'],
		"password": SYS_ACCOUNTS['BY']['password']
	}

	cur_domain = "http://www.aukeyit.com"

	sites = {
		"home": "http://www.aukeyit.com",
		"inventory": "http://supply-stock-report.aukeyit.com",
		"transfer_order": "http://supply-delivery.aukeyit.com",
		"new_product": "http://new-product.aukeyit.com",
	}

	s = None

	urls = {
		"login": {"url": "DOMAIN/login", "method": "POST"},
		"login_page": {"url": "DOMAIN/login", "method": "GET"},
		"center_inventory": {"url": "DOMAIN/report/centerStock/export?excelType=excel", "method": "GET"},
		"transfer_order_list": {"url": "DOMAIN/transfer/exportExcel", "method": "GET"},
		"product_list": {"url": "DOMAIN/query/list", "method": "GET"},
	}

	# ajax_header = {'X-Requested-With': 'XMLHttpRequest'}
	# csrf_header = {'X-CSRF-Token': ""}
	post_header = {'Content-Type': 'application/x-www-form-urlencoded'}

	headers = {
		'Referer': 'http://www.aukeyit.com/login',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
		'Cookie': ""
	}

	def __init__(self):
		self.s = requests.session()
		self.headers['Cookie'] = ""

		# login_status = self._check_login()
		# if not login_status:
		# self._login()
		self.login()

	def request(self, url_index, headers=None, data=None, params=None):
		# 封装requests库在当前类的使用
		# cookie 使用字符串加上分号结尾
		if data is None:
			data = {}
		if headers is None:
			headers = {}
		url_dict = copy.deepcopy(self.urls[url_index])
		url_dict['url'] = re.sub(r"DOMAIN", self.cur_domain, self.urls[url_index]['url'])
		cookies_dict = self._get_request_cookies()

		_d = ["ipCheck=true"]
		if "JSESSIONID" in cookies_dict:
			_d.append(f"JSESSIONID={cookies_dict['JSESSIONID']}")
		if "remember-me" in cookies_dict:
			_d.append(f"remember-me={cookies_dict['remember-me']}")

		self.headers['Cookie'] = ";".join(_d)
		request_headers = self.headers

		response = None
		request_data = data if data else {}
		request_headers = {**request_headers, **headers} if headers else request_headers
		request_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		if url_dict['method'] == "POST":
			response = self.s.post(url_dict['url'], data=request_data, headers=request_headers, params=params)
		elif url_dict['method'] == "GET":
			response = self.s.get(url_dict['url'], headers=request_headers, params=params)

		log = {
			"开始时间": request_start,
			"请求头": str(request_headers),
			"请求参数: ": {"params": params, "data": request_data},
			"cookies: ": str(self._get_request_cookies()),
			"返回cookies: ": str(requests.utils.dict_from_cookiejar(response.cookies)),
			"请求方式": str(url_dict),
			"请求响应: ": str(response.status_code),
			"请求返回头部": str(response.headers),
			"结束时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		}

		self.save_log(log)

		return response

	def login(self):
		encrypt = Encrypt()
		login_dict = copy.deepcopy(self.login_dict)
		login_dict['password'] = encrypt.get_aes_pass(self.login_dict['password'])

		# print(login_dict)
		headers = {**self.post_header}
		login_res = self.request('login', data=login_dict, headers=headers)

		# res_data = json.loads(login_res.content)
		if login_res.status_code == 200:
			print(u"登录成功")
			return True
		else:
			print(u"登录失败")
			raise RuntimeError(u"登录失败")
			# return False

	def save_log(self, content):
		""" 将爬取数据写入日志文件 """
		save_log(self.log, content, 'spider')

	def export_inventory(self, **kwargs):
		self.cur_domain = self.sites['inventory']
		stock_type = kwargs['stock_type'] if 'stock_type' in kwargs else 1
		target_date = kwargs['date'] if 'date' in kwargs else datetime.datetime.now().strftime("%Y-%m-%d")
		params = {
			"stockType": stock_type,
			"casGroup": "11,12056",  # 品牌四部和供应链四部
			"sku": "",
			"upc": "",
			"ids": "",
			"backUpDate": target_date,
			"material": ""
		}

		res = self.request("center_inventory", params=params)
		file_name = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")) + '.xls'
		cur_dir = os.path.join(BASE_LOG_DIR, self.log)
		file_path = os.path.join(cur_dir, file_name)
		if not os.path.exists(cur_dir):
			os.makedirs(cur_dir)
		with open(file_path, 'wb') as f:
			f.write(res.content)
		return file_path

	def _check_login(self):
		""" 检查是否已登录"""
		pass

	def _login(self):
		self.request('login_page')
		print(self.s.cookies)

	def _get_request_cookies(self):
		""" 获取request请求会话中的cookie """
		cookies = requests.utils.dict_from_cookiejar(self.s.cookies)
		return cookies

	def export_transfer_order(self, date=None):
		self.cur_domain = self.sites['transfer_order']
		target_date = date if date else datetime.datetime.now().strftime("%Y-%m-%d")
		params = {
			"pageSize": "100000000",
			"pageNumber": "1",
			"searchText": "undefined",
			"sortName": "undefined",
			"sortOrder": "asc",
			"limit": "100000000",
			"transferNo": "",
			"cabinetNo": "",
			"receivingCode": "",
			"isRece": "-1",
			"cabinetType": "",
			"transferSku": "",
			"transportType": "",
			"commonCarrier": "",
			"trialStatus": "",
			"outWarehouseId": "",
			"warehouseId": "",
			"isTax": "all",
			"transferUser": "",
			"transferBeginTime": target_date,
			"transferEndTime": target_date,
			"expectedBeginTime": "",
			"expectedEndTime": "",
			"transferStatus": "",
			"typeId": "all",
			"declarateStatus": "",
			"vatType": "",
			"isAbnormal": "",
			"offset": "undefined",
			"order": "undefined",
			"checked": ""
		}

		res = self.request("center_inventory", params=params)
		file_name = str("transfer_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")) + '.xls'
		cur_dir = os.path.join(BASE_LOG_DIR, self.log)
		file_path = os.path.join(cur_dir, file_name)
		if not os.path.exists(cur_dir):
			os.makedirs(cur_dir)
		with open(file_path, 'wb') as f:
			f.write(res.content)
		return file_path

	def export_product_list(self, **kwargs):
		params = {
			"pageSize": 20,
			"pageNumber": 1,
			"sortOrder": "asc",
			"sku_code": "",
			"sku_model": "",
			"org_id": "11%2C12056",  # 四部和供应链四部
			"dept_id": "",
			"develop_user_name": "",
			"update_user_name": "",
			"sealed_status": "",
			"sale_status":  "",
			"approve_status": "",
			"start_date": "",
			"end_date": "",
			"limit": 20000,
			"_": 1604111576331
		}
		self.cur_domain = self.sites['new_product']
		params['_'] = int(float(time.time()) * 1000)
		params['limit'] = kwargs['limit'] if "limit" in kwargs else 20

		res = self.request("product_list", params=params)
		if res.status_code == 200:
			return json.loads(res.content)
		else:
			raise RuntimeError("请求出错")

