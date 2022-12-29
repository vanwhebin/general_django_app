# _*_ coding: utf-8 _*_
# @Time     :   2020/9/8 14:27
# @Author       vanwhebin

from django.urls import re_path, include
from rest_framework import routers

from .views import UserViewSet, GroupViewSet, PermissionViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename="user")
router.register(r'group', GroupViewSet, basename="group")
router.register(r'permission', PermissionViewSet, basename="permission")

app_name = "usercenter"

urlpatterns = [
	re_path('', include(router.urls)),
]
