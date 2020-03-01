"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
from .settings_base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = "zhangtong_415@sina.com"
EMAIL_HOST_PASSWORD = '355caa8a60bb70e7'
# 与SMTP服务器进行通信，是否启动TLS链接（安全链接）
EMAIL_USE_SSL = True
# 注册有效期天数
CONFIRM_DAYS = 7