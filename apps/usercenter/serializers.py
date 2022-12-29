# _*_ coding: utf-8 _*_
# @Time     :   2020/9/14 12:40
# @Author       vanwhebin
# from abc import ABC
from abc import ABC

from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from django.contrib.auth.models import Permission, Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Media

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    # class Meta:
    #     __slots__ = ()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_superuser')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        # Token.objects.create(user=user)
        return user


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('file', 'size', 'create_time')



