import os

if os.getenv("DJANGO_ENV") != "ci":
    # mysql 设置
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            'NAME': os.getenv('MYSQL_DATABASE', default='django-bi'),
            'HOST': os.getenv('MYSQL_HOST', default='192.168.56.103'),
            'PORT': os.getenv('MYSQL_PORT', default='3306'),
            'USER': os.getenv('MYSQL_USER', default='root'),
            'PASSWORD': os.getenv('MYSQL_PASSWORD', default='root'),     
            "OPTIONS": {
                "autocommit": True,
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                "charset": "utf8mb4",
            }
        }
    }
