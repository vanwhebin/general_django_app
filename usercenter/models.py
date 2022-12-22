import os

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models
from workApp.settings import UPLOAD_MEDIA_CHOICES, MEDIA_ROOT


class UserManager(BaseUserManager):

    def _create_user(self, username, password, email, **kwargs):
        if not username:
            raise ValueError(u"请输入用户名")
        if not password:
            raise ValueError(u"请输入密码")
        if not email:
            raise ValueError(u"请输入邮箱地址")

        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, email, **kwargs)

    def create_superuser(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        kwargs['is_active'] = True
        return self._create_user(username, password, email, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_TYPE = (
        ('1', '男'),
        ('2', '女'),
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, verbose_name="用户名", unique=True)
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name="昵称")
    gender = models.CharField(max_length=10, choices=GENDER_TYPE, null=True, blank=True, verbose_name="性别")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="电话号码")
    email = models.EmailField(verbose_name="邮箱", unique=True)
    picture = models.ImageField(upload_to="profile/%Y/%m/%d", null=True, blank=True, verbose_name="头像")
    wx_token = models.CharField(max_length=200, null=True, blank=True, verbose_name="微信令牌")
    dd_token = models.CharField(max_length=200, null=True, blank=True, verbose_name="钉钉令牌")
    is_active = models.BooleanField(default=False, verbose_name="状态")
    is_staff = models.BooleanField(default=True, verbose_name="是否是员工")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_group",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_permission",
        related_query_name="user",
    )

    # USERNAME_FIELD = 'username'
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.nickname if self.nickname else self.username

    class Meta:
        verbose_name = "user"
        verbose_name_plural = verbose_name
        db_table = "auth_user"


class Menu(models.Model):
    """ menu """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name="菜单显示名称", default="", blank=True)
    name = models.CharField(max_length=50, verbose_name="菜单标识名称", default="")
    url = models.CharField(max_length=50, default="", blank=True, verbose_name="菜单前台路由")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="菜单前台路由")
    icon = models.CharField(max_length=100, default="", blank=True, verbose_name="菜单显示图标")
    file = models.CharField(max_length=100, default="", verbose_name="菜单所属前台组件地址")
    show_in_menu = models.BooleanField(default=True, blank=True, verbose_name="是否在后台菜单中显示")
    not_cache = models.BooleanField(default=False, blank=True, verbose_name="是否缓存当前页面")
    redirect = models.CharField(default="", blank=True, max_length=100, verbose_name="页面不存在或无权限下重定向页面")
    order = models.PositiveSmallIntegerField(default=1, blank=True, verbose_name="排序")
    is_code = models.BooleanField(default=False, blank=True, verbose_name="是否必须扫码才可见")

    class Meta:
        ordering = ('-order',)

    def __str__(self):
        return self.title


class Locale(models.Model):
    """ Locale 语言包 """
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=50, verbose_name='语言包的代号')
    value = models.CharField(max_length=200, verbose_name='语言包的对应语言内容')
    lang = models.CharField(max_length=15, verbose_name='语种', default='zh-CN')

    def __str__(self):
        return self.value


class Media(models.Model):
    """ 媒体文件库 """

    class Meta:
        ordering = ('-create_time',)
        index_together = ("hash", "size")

    def __str__(self):
        return self.file

    id = models.AutoField(primary_key=True)
    file = models.FileField(max_length=200, upload_to="%Y-%m-%d", verbose_name="文件地址")
    size = models.PositiveIntegerField(verbose_name="文件大小", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="uploader", verbose_name="上传用户")
    extension = models.CharField(max_length=10, verbose_name="文件扩展名", choices=UPLOAD_MEDIA_CHOICES)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    hash = models.CharField(max_length=200, verbose_name="文件哈希", null=True, blank=True)

