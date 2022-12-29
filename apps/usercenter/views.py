# _*_ coding: utf-8 _*_
# @Time     :   2020/8/31 20:17
# @Author       vanwhebin

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from usercenter.serializers import UserSerializer, GroupSerializer, PermissionSerializer, \
	MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsAdminUser, )


class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	permission_classes = (IsAdminUser,)


class PermissionViewSet(viewsets.ModelViewSet):
	queryset = Permission.objects.all()
	serializer_class = PermissionSerializer
	permission_classes = (IsAdminUser,)

