# _*_ coding: utf-8 _*_
# @Time     :   2020/9/3 17:03
# @Author       vanwhebin
from __future__ import absolute_import, unicode_literals
import arrow
import os
import hashlib
import time
import pytz
import datetime
from uuid import uuid4
from base64 import urlsafe_b64encode
from rest_framework import status

from django.http import JsonResponse
from workApp.settings import TIME_ZONE, BASE_LOG_DIR


def uuid():
    # 生成uuid
    return urlsafe_b64encode(uuid4().bytes).decode("ascii").rstrip("=")


def get_all_day_per_year(years, start_date=None, end_date=None):
    """ 日期范围内的时间日期列表 """
    start_date = start_date or f'{years}-1-1'
    end_date = end_date or time.strftime("%Y-%m-%d")
    start = 0
    all_date_list = []
    days_sum = 365
    while start < days_sum:
        b = arrow.get(start_date).shift(days=start).format("YYYY-MM-DD")
        start += 1
        if b > end_date:
            break
        all_date_list.append(b)
    # print(all_date_list)
    return all_date_list


def get_yesterday(day=1):
    """ 获取昨天日期 """
    return (datetime.datetime.now(pytz.timezone(TIME_ZONE)) - datetime.timedelta(days=day)).strftime("%Y-%m-%d")


def response(data="", status_code=status.HTTP_200_OK, code=0, **kwargs):
    """ 格式化返回信息 """
    res = {
        "code": code,
        "msg": "ok",
        "data": data,
    }
    res.update(kwargs)
    return JsonResponse(res, status=status_code)


def save_log(directory, content, log_type=None):
    """ 将爬取数据写入日志文件 """
    log_file = str(log_type) + "_" + time.strftime("%Y%m%d", time.localtime(time.time())) + '.log'
    cur_dir = os.path.join(BASE_LOG_DIR, directory)

    if not os.path.exists(cur_dir):
        os.makedirs(cur_dir)
    with open(os.path.join(cur_dir, log_file), 'a+', encoding="utf-8") as f:
        f.write(str(content) + os.linesep)


def get_md5_hash(file_path, blocksize=65536):
    """
    :param file_path: 文件路径
    :param blocksize: 文件块大小
    :return:
    """
    hash_handler = hashlib.md5()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash_handler.update(block)
    return hash_handler.hexdigest()


