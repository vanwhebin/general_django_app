# _*_ coding: utf-8 _*_
# @Time     :   2020/9/24 21:43
# @Author       vanwhebin

from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    page_query_param = "page"
