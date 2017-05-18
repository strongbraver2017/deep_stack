# -*- coding: utf-8 -*-
"""
@file:      models.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.5
@editor:    Vim
@create:    3/26/17 7:28 PM
@description:
        用户行为以及反爬虫工作记录表模型，反爬仅过滤IP。
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class RequestRecord(models.Model):
    """
    此表是持久化记录用户访问行为的工作表。
    """
    ip = models.CharField("用户IP", max_length=20)
    user = models.ForeignKey(User, null=True, verbose_name="用户")
    time = models.DateTimeField(default=timezone.now, verbose_name="访问时间")
    method = models.CharField(max_length=100, verbose_name="访问请求函数")
    kwargs = models.CharField(max_length=255, verbose_name="传参列表", null=True)
    returns = models.CharField(max_length=255, verbose_name="运行结果", null=True)


class RecentIpActivity(models.Model):
    """
    此表是临时统计最近用户访问恶意行为的工作表。
    """
    ip = models.CharField("用户IP", max_length=20, unique=True)
    visits_in_period = models.IntegerField("周期内访问次数", default=0)
    destroy_time = models.DateTimeField(verbose_name="预定移除时间")


class Ban(models.Model):
    """
    此表存储被封禁的用户IP。
    """
    ip = models.CharField("封禁用户IP", max_length=20, unique=True)
    ban_to = models.DateTimeField(verbose_name="解除封禁时间")


class VerifyCode(models.Model):
    """
    此表存储通过手机和邮箱验证身份的通行证（可以关联账户）。
    """
    user = models.ForeignKey(User, verbose_name="关联账户", null=True)
    code = models.CharField("通行证", max_length=100)
    invalid_time = models.DateTimeField("失效时间")

    def __str__(self):
        return self.code
