# -*- coding: utf-8 -*-
"""
@file:      utils.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.5
@editor:    Vim
@create:    3/29/17 2:04 AM
@description:
        用于反爬虫的一些过滤方法
"""

from django.contrib.auth.models import AnonymousUser
from .models import RecentIpActivity, RequestRecord, Ban, VerifyCode
from django.utils import timezone
from datetime import timedelta
from DjiStudio.settings import PERIOD_MINUTES, BAN_IP_RQUEST_LIMIT, BAN_HOURS
from django.http import HttpResponseForbidden
from random import Random


def get_client_ip(request):
    """得到客户端请求的源IP。
    
    :param request: 
    :return: 
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def filter_ip(method_name=None, use_ban=False):
    """过滤访问者IP的view func装饰器。
        
        1.用于反爬虫或恶意请求。
        2.考虑到Dji Studio网站的初期运营，只封ip,不封用户。
        
    :param method_name: 
    :param use_ban: 
    :return: 
    """
    def decrator(view_func):

        def wrapper(request):

            ip = get_client_ip(request)

            # IP若属于封禁列表，则返回403
            for ban in Ban.objects.filter(ip=ip):
                if timezone.now() < ban.ban_to:
                    return HttpResponseForbidden()

            user = None if isinstance(request.user, AnonymousUser) else request.user
            method = method_name if method_name else view_func.__name__

            # 创建持久化访问记录（用户行为表）
            RequestRecord.objects.create(ip=ip, user=user, method=method)

            # 检索周期内访问记录
            if RecentIpActivity.objects.filter(ip=ip).count() == 0:
                # 周期内第一次访问，则创建记录
                new_activity = RecentIpActivity()
                new_activity.ip = ip
                new_activity.visits_in_period = 0
                new_activity.destroy_time = timezone.now() + timedelta(minutes=PERIOD_MINUTES)
                new_activity.save()
            else:
                # 其余则令访问次数自增
                activity = RecentIpActivity.objects.filter(ip=ip).first()
                activity.visits_in_period += 1
                activity.save()

                # 若大于访问限额，则在Ban表（黑名单）中创建对象
                if use_ban and activity.visits_in_period > BAN_IP_RQUEST_LIMIT:
                    Ban.objects.create(ip=ip, ban_to=timezone.now() + timedelta(hours=BAN_HOURS))

            return view_func(request)

        return wrapper

    return decrator


def verify_is_ok(verify_code, user_email):
    """基本的通行证校验逻辑。

    :param user_email: 用户邮箱
    :param verify_code: 通行证
    :return: Boolean: 是否通过
    """
    validate_kwargs = dict()
    validate_kwargs['code'] = verify_code
    validate_kwargs['user__email'] = user_email
    verify_codes = VerifyCode.objects.filter(**validate_kwargs)
    err_msg = None

    if not verify_codes:
        err_msg = "none this verify_code"
    for verify in verify_codes:
        if verify.invalid_time > timezone.now():
            return True, None
        else:
            err_msg = "verify_code timeout"

    return False, err_msg


def random_str(randomlength=8,
               just_number=False):
    """生成固定长度随机字符串。

    :param      randomlength: 输出随机字串的长度
    :param      just_number: 仅生成数字
    :return:
    """

    string = ""

    if just_number:
        chars = '0123456789'
    else:
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'

    length = len(chars) - 1
    random = Random()

    for i in range(randomlength):
        string += chars[random.randint(0, length)]

    return string


def generate_email_code(randomlength=16, just_number=False):
    # 生成用于邮件校验的通行令牌。
    return random_str(randomlength=randomlength, just_number=just_number)


def generate_sms_code(randomlength=6, just_number=True):
    # 生成用于短信校验的通行令牌。
    return random_str(randomlength=randomlength, just_number=just_number)