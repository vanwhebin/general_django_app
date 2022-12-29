# _*_ coding: utf-8 _*_
# @Time     :   2020/10/7 11:26
# @Author       vanwhebin

from django.views.generic import View
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer

from libs.qywx.conf import Conf
from libs.qywx.CorpApi import CorpApi, CORP_API_TYPE
from apps.usercenter.models import UserManager, User
from utils.util import response


class WxRequiredMixin(View):
    """ 验证是否企业微信登录成功；"""

    def dispatch(self, request, *args, **kwargs):
        # 状态和文章实例有user属性
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied

        return super(WxRequiredMixin, self).dispatch(request, *args, **kwargs)


class WxPushHelper:
    api = None

    def __init__(self):
        self.api = CorpApi(Conf['CORP_ID'], Conf['APP_SECRET'])

    def get_corp_user_id_by_code(self, code):
        return self.api.httpCall(CORP_API_TYPE['GET_USER_INFO_BY_CODE'], {"CODE": code})

    def get_user_info_by_corp_user_id(self, corp_user_id):
        return self.api.httpCall(CORP_API_TYPE['USER_GET'], {'userid': corp_user_id})

    def push_text(self, user_wx_id, content):
        data = {
            "agentid": Conf['APP_ID'],  # 企业应用ID
            "msgtype": 'text',  # 消息类型为文本
            "touser": user_wx_id,  # 接受消息的对象
            "text": {
                "content": content  # 消息文本
            }
        }
        return self.api.httpCall(CORP_API_TYPE['MESSAGE_SEND'], data)

    def push_card(self, user_wx_id, url, description):
        data = {
            "touser": str(user_wx_id),
            "msgtype": "textcard",
            "agentid": Conf['APP_ID'],  # 企业应用ID
            "textcard": {
                "title": "产品立项流程通知",
                "description": description,
                "url": url,
                "btntxt": "点击查看"
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }

        return self.api.httpCall(CORP_API_TYPE['MESSAGE_SEND'], data)


class WxUserlogin(APIView):
    allowed_methods = ['POST']
    permission_classes = (AllowAny, )

    @staticmethod
    def _get_user_info(code):
        client = WxPushHelper()
        corp_user = client.get_corp_user_id_by_code(code)
        if "errcode" in corp_user and corp_user['errcode'] == 0 and "UserId" in corp_user:
            return client.get_user_info_by_corp_user_id(corp_user['UserId'])
        else:
            raise RuntimeError(u"获取企业微信用户信息错误")

    def post(self, request, *args, **kwargs):
        code = request.data.get('code', '').strip()
        if not code:
            raise PermissionDenied
        else:
            info = self._get_user_info(code)
            user = User.objects.filter(wx_token=info['userid']).first()
            if not user:
                user = User.objects.create(
                    username=info['name'],
                    email=info['email'],
                    wx_token=info['userid'],
                    is_active=True
                )
                user.set_password("123456")
                user.save()
            # 获取token
        token_obj = TokenObtainPairSerializer.get_token(user)
        return response({"access_token": str(token_obj.access_token)})




