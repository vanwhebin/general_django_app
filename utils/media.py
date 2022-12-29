# _*_ coding: utf-8 _*_
# @Time     :   2022/12/29 16:33
# @Author       vanwhebin
from __future__ import absolute_import, unicode_literals

import os
import time

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import response, status

from apps.usercenter.serializers import MediaSerializer
from apps.usercenter.models import Media
from configs.default.media import UPLOAD_MEDIA_CHOICES
from configs.default.common import MEDIA_ROOT
from utils.util import uuid, get_md5_hash


class UploadMedia(CreateAPIView):
	# queryset = Media
	serializer_class = MediaSerializer
	permission_classes = (AllowAny, )

	def post(self, request, *args, **kwargs):
		super(UploadMedia, self).__init__()
		uploaded_file = request.FILES.get('file')
		uploaded_file.name = uploaded_file.name.strip('"')

		if not uploaded_file:
			return response.Response(u"文件上传失败", status=status.HTTP_400_BAD_REQUEST)
		ext_pos = uploaded_file.name.rfind('.')
		uploaded_file_ext = uploaded_file.name[ext_pos:]
		if not self.allowed_extension(uploaded_file_ext):
			return response.Response(u"非法文件类型", status=status.HTTP_400_BAD_REQUEST)
		hash_file_name = uuid() + uploaded_file_ext
		time_tag = time.strftime('%Y-%m-%d')
		file_path = time_tag + os.sep + hash_file_name
		dir_path = os.path.join(MEDIA_ROOT, time_tag)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		with open(os.path.join(dir_path, hash_file_name), 'wb') as f:
			f.write(uploaded_file.read())

		file_hash = get_md5_hash(os.path.join(dir_path, hash_file_name))
		file_size = int(uploaded_file.size / 1024)
		file = Media.objects.filter(hash=file_hash, size=file_size).first()
		if not file:
			file = Media.objects.create(
				file=uploaded_file,
				hash=file_hash,
				# user=request.user,
				size=file_size,
				extension=uploaded_file_ext
			)
		os.remove(os.path.join(MEDIA_ROOT, file_path))
		return response.Response(MediaSerializer(file, context={'request': request}).data)

	@staticmethod
	def allowed_extension(ext):
		choices = UPLOAD_MEDIA_CHOICES
		for allowed_ext in choices:
			if ext == allowed_ext[0]:
				return True
		return False

	def allowed_file_size(self, size):
		pass


