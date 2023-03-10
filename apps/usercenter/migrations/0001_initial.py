# Generated by Django 4.1.4 on 2022-12-21 01:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='用户名')),
                ('nickname', models.CharField(blank=True, max_length=50, null=True, verbose_name='昵称')),
                ('gender', models.CharField(blank=True, choices=[('1', '男'), ('2', '女')], max_length=10, null=True, verbose_name='性别')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='电话号码')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='profile/%Y/%m/%d', verbose_name='头像')),
                ('wx_token', models.CharField(blank=True, max_length=200, null=True, verbose_name='微信令牌')),
                ('dd_token', models.CharField(blank=True, max_length=200, null=True, verbose_name='钉钉令牌')),
                ('is_active', models.BooleanField(default=False, verbose_name='状态')),
                ('is_staff', models.BooleanField(default=True, verbose_name='是否是员工')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_group', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_permission', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'user',
                'db_table': 'auth_user',
            },
        ),
        migrations.CreateModel(
            name='Locale',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=50, verbose_name='语言包的代号')),
                ('value', models.CharField(max_length=200, verbose_name='语言包的对应语言内容')),
                ('lang', models.CharField(default='zh-CN', max_length=15, verbose_name='语种')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default='', max_length=50, verbose_name='菜单显示名称')),
                ('name', models.CharField(default='', max_length=50, verbose_name='菜单标识名称')),
                ('url', models.CharField(blank=True, default='', max_length=50, verbose_name='菜单前台路由')),
                ('icon', models.CharField(blank=True, default='', max_length=100, verbose_name='菜单显示图标')),
                ('file', models.CharField(default='', max_length=100, verbose_name='菜单所属前台组件地址')),
                ('show_in_menu', models.BooleanField(blank=True, default=True, verbose_name='是否在后台菜单中显示')),
                ('not_cache', models.BooleanField(blank=True, default=False, verbose_name='是否缓存当前页面')),
                ('redirect', models.CharField(blank=True, default='', max_length=100, verbose_name='页面不存在或无权限下重定向页面')),
                ('order', models.PositiveSmallIntegerField(blank=True, default=1, verbose_name='排序')),
                ('is_code', models.BooleanField(blank=True, default=False, verbose_name='是否必须扫码才可见')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usercenter.menu', verbose_name='菜单前台路由')),
            ],
            options={
                'ordering': ('-order',),
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=200, upload_to='%Y-%m-%d', verbose_name='文件地址')),
                ('size', models.PositiveIntegerField(blank=True, null=True, verbose_name='文件大小')),
                ('extension', models.CharField(choices=[('.pdf', 'PDF'), ('.xlsx', 'EXCEL'), ('.xls', 'EXCEL'), ('.doc', 'DOC'), ('.docx', 'DOC'), ('.ppt', 'PPT'), ('.png', 'IMAGE'), ('.jpg', 'IMAGE')], max_length=10, verbose_name='文件扩展名')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('hash', models.CharField(blank=True, max_length=200, null=True, verbose_name='文件哈希')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploader', to=settings.AUTH_USER_MODEL, verbose_name='上传用户')),
            ],
            options={
                'ordering': ('-create_time',),
                'index_together': {('hash', 'size')},
            },
        ),
    ]
