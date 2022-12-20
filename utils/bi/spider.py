# _*_ coding: utf-8 _*_
# @Time     :   2020/8/21 15:02
# @Author       vanwhebin
import time
import json
from lxml import etree
import re
import copy

from bs4 import BeautifulSoup as bs
import requests
from django.core.cache import cache

from workApp.settings import SYS_ACCOUNTS
from .rsa_encrypt import Encrypt
from utils.util import get_yesterday, save_log


class DataSpider:
	log = 'bi'
	login_dict = {
		"email": SYS_ACCOUNTS['BI']['username'],
		"password": SYS_ACCOUNTS['BI']['password']
	}

	site_urls = {
		1: "http://sky.aukeyit.com",
		2: "http://superstar.aukeyit.com",
	}
	cookie_cache_prefix = 'bi_login_cookie_'
	cookie_identity_key = '_identity'
	cookie_cache_timeout = (3600 * 24)
	cur_domain = None

	urls = {
		"dashboard": {"url": "DOMAIN//dashboard/index", "method": "GET", 'ajax': False},
		"login": {"url": "DOMAIN/user/login", "method": "POST", 'ajax': True},
		"login_page": {"url": "DOMAIN/user/login", "method": "GET"},
		"logout": {"url": "DOMAIN/user/logout", "method": "POST"},
		"sales_info": {"url": "DOMAIN/amazon/dashboard/trend-ajax", "method": "POST", 'ajax': True},
		"sales_live_data": {"url": "DOMAIN/amazon/immediate-sales-report/data-ajax-bi", "method": "POST", 'ajax': True},
		"sales_trend": {"url": "DOMAIN/amazon/dashboard/trend", "method": "GET"},
		"report": {"url": "DOMAIN/amazon/dashboard/report", "method": "GET", 'ajax': False},
		"sales_team_aggregation": {"url": "DOMAIN/amazon/dashboard/team-report", "method": "GET"},
		"group": {"url": "DOMAIN/amazon/team/index", "method": "GET"},
		"product": {"url": "DOMAIN/amazon/product/download", "method": "GET"},
		"listing": {"url": "DOMAIN/amazon/dashboard/listing-rank-ajax", "method": "POST", 'ajax': True},
		"brand": {"url": "DOMAIN/amazon/brand/index", "method": "GET"},
		"target": {"url": "DOMAIN/amazon/team-goal/index", "method": "GET"},
	}

	ajax_header = {'X-Requested-With': 'XMLHttpRequest'}
	csrf_header = {'X-CSRF-Token': ""}
	post_header = {'Content-Type': 'application/x-www-form-urlencoded'}

	headers = {
		'Referer': 'DOMAIN/user/login',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
		'Cookie': ""
	}

	sales_query_params = {
		"type": "",
		"startDate": "",
		"endDate": "",
		"amazonIds": "",
		"teamIds": "",
		"teamUserIds": "",
		"productName": "",
		"edSku": "",
		"asin": "",
		"devTeamIds": "",
		"developUserIds": "",
		"category": "",
		"level": "",
	}

	s = None

	def __init__(self, **kwargs):
		self.s = requests.session()
		site_id = kwargs['site_id'] if "site_id" in kwargs and kwargs['site_id'] else 1
		self.headers['Cookie'] = ""

		if "_csrf" in self.s.headers:
			del self.s.headers['_csrf']
		if "_identity" in self.s.headers:
			del self.s.headers['_identity']

		self.cur_domain = self.site_urls.get(int(site_id))
		login_status = self._check_login()
		if not login_status:
			self.login()

	def request(self, url_index, headers=None, data=None, params=None):
		# 封装requests库在当前类的使用
		# cookie 使用字符串加上分号结尾
		url_dict = copy.deepcopy(self.urls[url_index])
		url_dict['url'] = re.sub(r"DOMAIN", self.cur_domain, self.urls[url_index]['url'])

		_d = []
		# if "PHPSESSID" in self.s.cookies:
		if cache.get(f"{self.cookie_cache_prefix}PHPSESSID"):
			psd = cache.get(f"{self.cookie_cache_prefix}PHPSESSID")
			# psd = self.s.cookies['PHPSESSID']
			_d.append(f"PHPSESSID={psd}")
		# if "_csrf" in self.s.cookies:
		if cache.get(f"{self.cookie_cache_prefix}_csrf"):
			csrf = cache.get(f"{self.cookie_cache_prefix}_csrf")
			# _d.append(f"_csrf={self.s.cookies['_csrf']}")
			_d.append(f"_csrf={csrf}")

		# if "_identity" in self.s.cookies:
		if cache.get(f"{self.cookie_cache_prefix}{self.cookie_identity_key}"):
			# if cache.get(f"{self.cookie_cache_prefix}_identity"):
			# 	_id = cache.get(f"{self.cookie_cache_prefix}_identity")
			# if "_identity" in self.s.cookies:
			# 	_id = self.s.cookies['_identity']
			_id = cache.get(f"{self.cookie_cache_prefix}{self.cookie_identity_key}")
			_d.append(f"_identity={_id}")
		self.headers['Cookie'] = ";".join(_d)
		request_headers = self.headers
		request_headers['Referer'] = f'{self.cur_domain}/user/login'
		response = None
		request_data = data if data else {}
		request_headers = {**request_headers, **headers} if headers else request_headers

		request_start = time.strftime("%Y-%m-%d %H:%M:%S")

		if url_dict['method'] == "POST":
			if url_index != 'login':
				request_headers['X-CSRF-Token'] = self._get_csrf_token()

			response = self.s.post(url_dict['url'], data=request_data, headers=request_headers, params=params)
		elif url_dict['method'] == "GET":
			response = self.s.get(url_dict['url'], headers=request_headers, params=params)

		cookies = self._get_request_cookies()
		for key, value in cookies.items():
			cache.set(f"{self.cookie_cache_prefix}{key}", value)

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

	def login(self):
		csrf_token = self._get_csrf_token()
		encrypt = Encrypt()
		login_dict = copy.deepcopy(self.login_dict)
		self.csrf_header['X-CSRF-Token'] = csrf_token
		login_dict['password'] = encrypt.get_rsa_pass(self.login_dict['password'])
		# del encrypt
		# print(login_dict)
		headers = {**self.post_header, **self.ajax_header, **self.csrf_header}
		login_res = self.request('login', data=login_dict, headers=headers)
		if login_res.status_code == 200:
			res_data = json.loads(login_res.content)
			cookies = self._get_request_cookies()
			cache.set(f"{self.cookie_cache_prefix}{self.cookie_identity_key}", cookies[self.cookie_identity_key],
			          timeout=self.cookie_cache_timeout)
			print(u"登录成功" + str(res_data))
			return True
		else:
			print(u"登录失败" + str(login_res.content))
			return False

	def _get_request_cookies(self):
		""" 获取request请求会话中的cookie """
		cookies = requests.utils.dict_from_cookiejar(self.s.cookies)
		return cookies

	def _check_login(self):
		""" 检查是否已登录"""
		return bool(cache.get(f"{self.cookie_cache_prefix}{self.cookie_identity_key}"))

	def _get_csrf_token(self):
		url_index = "dashboard" if self._check_login() else "login_page"
		login_page = self.request(url_index)
		soup = bs(login_page.content, features='html.parser', from_encoding='utf-8')
		csrf_token = soup.head.find(attrs={"name": "csrf-token"}).get('content')
		return csrf_token

	def logout(self):
		return self.request('logout')

	def get_sales_info(self, **kwargs):
		# 销售明细  date dep_type=4

		date = kwargs['date'] if "date" in kwargs else get_yesterday()
		dep_type = kwargs['dep_type'] if "dep_type" in kwargs else 4
		# yesterday = startDate if startDate and endDate else get_yesterday()
		kwargs = {
			"type": dep_type,
			"startDate": date,
			"endDate": date
		}
		data = {**self.sales_query_params, **kwargs}
		sales_info_res = self.request('sales_info', data=data, headers={**self.ajax_header, **self.csrf_header})
		if sales_info_res.status_code == 200:
			return json.loads(sales_info_res.content)
		else:
			return []

	def get_products_list(self):
		pass

	def get_sales_team_report(self, **kwargs):
		"""  获取销售小组预报 """
		headers = {**self.post_header, **self.ajax_header}
		sales_report = self.request('listing', data={"startDate": kwargs['date']}, headers=headers)
		if sales_report.status_code == 200:
			return json.loads(sales_report.content)
		else:
			print(sales_report.content)
			return False

	def get_sales_report(self, **kwargs):
		"""
		@:param start_date
		@:param end_date
		@:param site_id
		获取销售预报
		"""
		start_date = kwargs['start_date'] if "start_date" in kwargs else get_yesterday()
		end_date = kwargs['end_date'] if "end_date" in kwargs else get_yesterday()
		params = {"start_date": start_date, "end_date": end_date}
		response = self.request('report', params=params)
		if response.status_code == 200:
			selector = etree.HTML(response.content)
			items = selector.xpath('//*[@id="amazon_total"]/tbody/tr')
			rows = []
			for row in items:
				tds = row.xpath('td')
				i = [re.sub(r"\s|,", "", item.xpath("string(.)")) for item in tds]
				rows.append(i)
			return rows
		else:
			return False

	def save_log(self, content):
		""" 将爬取数据写入日志文件 """
		save_log(self.log, content, 'spider')

	def get_sales_group(self):
		# 获取所有的销售小组和销售人员信息
		group_page = self.request('group')
		table = []

		soup = bs(group_page.content, features='html.parser', from_encoding='utf-8')
		trs = soup.find(id="team_table_1").find("tbody").find_all('tr')
		for tr in trs:
			column = []
			tds = tr.find_all('td')
			for i in range(1, 5):
				column.append(str(tds[i].string or ''))
			table.append(column)
		return table

	def get_brands(self):
		# 获取所有的品牌分类信息
		brands = []
		self.cur_domain = self.site_urls[1]
		brand_page = self.request('brand')
		soup = bs(brand_page.content, features='html.parser', from_encoding='utf-8')
		brand_count = len(soup.find(id="w1").find_all('li')) - 2  # 去掉前一页和后一页
		if brand_count > 0:
			# 从第二页进行循环
			for page in range(1, (brand_count + 1)):
				brands.extend(self._get_brands(page))

		else:
			brands.extend(self._get_brands())
		return brands

	def _get_brands(self, page=1):
		# 返回一个品牌列表
		column = []
		brand_page = self.request('brand', params={"page": f'{page}'})
		soup = bs(brand_page.content, features='html.parser', from_encoding='utf-8')
		trs = soup.tbody.find_all("tr")
		for i in trs:
			column.append(i.find("td").next_sibling.string)
		return column

	def get_sales_target(self):
		targets = []
		target_page = self.request('target')
		soup = bs(target_page.content, features='html.parser', from_encoding="utf-8")
		target_table = soup.find(attrs={"class": "goal-index"}).find_all('table')[0]
		trs = target_table.find_all('tr')
		lens = len(trs) - 1
		for i in range(2, lens):
			column = []
			tds = trs[i].find_all('td')
			for td in tds:
				column.append(re.sub(r'\s', '', td.string))
			targets.append(column)
		return targets

	def get_sales_team_aggregation(self):
		""" 爬取销售小组预报的汇总信息 """
		response = self.request('sales_team_aggregation')
		if response.status_code == 200:
			selector = etree.HTML(response.content)
			items = selector.xpath('//*[@id="team_stat_table"]/tfoot/tr/td')
			agg_list = [re.sub(r"\s", "", item.xpath("string(.)")) for item in items][1:]
			return agg_list
		else:
			raise RuntimeError("请求销售预报链接出错")

	def get_live_sales_data(self):
		""" 爬取实时销售数据 """
		query_data = {
			"marketplaceIds": "",
			"companyIds": '',
			"todayDate": ''
		}
		headers = {**self.post_header, **self.ajax_header, **self.csrf_header, **{"Content-Length": "38"}}
		response = self.request('sales_live_data', data=query_data, headers=headers)
		if response.status_code == 200:
			return json.loads(response.content)
		else:
			return []
