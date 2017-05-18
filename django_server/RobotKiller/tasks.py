# -*- coding: utf-8 -*-
"""
@file:      tasks.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.5
@editor:    Vim
@create:    3/29/17 2:20 AM
@description:
        用于反爬虫的一些异步任务，主要是刷新数据表中某些临时记录。
"""
from __future__ import absolute_import, unicode_literals
from celery import task as celery_task
from .models import Ban, RecentIpActivity
from django.utils import timezone


@celery_task(name="refresh_ban")
def refresh_ban():
    clear_bans = []
    for ban in Ban.objects.all():
        if ban.ban_to < timezone.now():
            ban.delete()
            print("clear {} from Ban".format(ban.ip))
            clear_bans.append(ban.ip)

    return clear_bans


@celery_task(name="refresh_ip_activity")
def refresh_ip_activity():
    clear_act_ips = []
    for ip_activity in RecentIpActivity.objects.all():
        if ip_activity.destroy_time < timezone.now():
            ip_activity.delete()
            print("clear {} acts from activities".format(ip_activity.ip))
            clear_act_ips.append(ip_activity.ip)

    return clear_act_ips
