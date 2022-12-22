# _*_ coding: utf-8 _*_
# @Time     :   2020/9/14 11:54
# @Author       vanwhebin

from django.urls import path, re_path, include
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from usercenter.views import MyTokenObtainPairView
from utils.media import UploadMedia
from workApp.settings import MEDIA_URL, MEDIA_ROOT, API_VERSION, STATIC_URL, STATIC_ROOT


urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    path(API_VERSION + 'auth/', include('usercenter.urls', namespace='usercenter')),
    path(API_VERSION + 'upload/', UploadMedia.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(API_VERSION + 'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(API_VERSION + 'token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
] + static(STATIC_URL, document_root=STATIC_ROOT)
