# -*- coding: utf-8 -*-
"""
@file:      views.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.5
@editor:    Vim
@create:    3/21/17 3:35 AM
@description:
        针对与公共api通用view的写法封装。
"""

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from datetime import date
import copy
import json
import inspect

from ..RobotKiller.utils import filter_ip
from ..RobotKiller.models import RequestRecord


def transfer_value_type(trans_type, value):
    if trans_type == date:
        if "-" not in value:
            raise TypeError("Date type use like: `2016-07-13`")
        else:
            y, m, d = [int(ymd.strip()) for ymd in value.split("-")]
            return date(year=y, month=m, day=d)

    elif trans_type == list:
        if "," not in value:
            raise TypeError("List type use like: `1,2,3`")
        else:
            return [int(ele) for ele in value.split(",")]

    else:
        return trans_type(value)


def get_func_standard_and_necessary_keys(func):
    """得到某个function的形参列表.

    :param func: 任意函数
    :return: standard_keys:标准形参就是所有形参
             necessary_keys: 必要形参就是没给默认值的形参。
    """
    standard_kwargs = dict(inspect.signature(func).parameters)
    necessary_keys = []

    for k, v in standard_kwargs.items():
        format_string = v.__str__()
        if "=" in format_string:
            standard_kwargs[k] = format_string.split("=")[-1]
        else:
            standard_kwargs[k] = None
            necessary_keys.append(k)

    return set(standard_kwargs.keys()), set(necessary_keys)


def my_api_view(
        process_data_func,
        http_method="GET",
        permissions=[AllowAny],
        api_internal_debug=False,
        white_parameter_extend=[],
        key_type_map={}
):
    """通用公共api聚合装饰器。

        包括以下几个方面：
            １．数据库ORM逻辑封装为process_data_func，专注于写业务即可。
            ２．连接反爬虫模块的filter ip方法，即每个用此装饰器的view方法会被全部记录用户行为。
            ３．对于RESTful Framework提供的api_view做了简易封装，
                返回也是该包提供的Response对象。

    :param process_data_func: 处理数据库ORM逻辑的函数
    :param http_method: 可访问的方式：　["GET", "POST", ...]
    :param permissions: 见　RESTful Framework　的权限配置
    :param api_internal_debug: api内部debug用于api异常时开发者发现具体报错位置
    :param white_parameter_extend: 外加参数白名单
    :param key_type_map: 强制类型转化哈希表,例如:
                                key_type_map={
                                    "begin_date": date,
                                    "end_date": date,
                                    "view_days": int,
                                    "solution_id": int,
                                }
    :return: Response对象
    """

    white_parameters = ['format', 'csrfmiddlewaretoken', ]
    white_parameters.extend(white_parameter_extend)
    request_method_map = {
        "GET": "query_params",
        "POST": "data"
    }

    def decorator(view_func):
        @filter_ip(method_name=process_data_func.__name__)
        @api_view(http_method_names=[http_method, ])
        @permission_classes(permissions)
        def wrapper(request):
            receive_kwargs = {}
            for k, v in getattr(request, request_method_map[http_method.upper()]).items():
                receive_kwargs[k] = v

            origin_kwargs = copy.deepcopy(receive_kwargs)

            ret = {"data": None, "err_msg": None, "received": receive_kwargs}

            standard_keys, necessary_keys = get_func_standard_and_necessary_keys(process_data_func)

            receive_keys = set(receive_kwargs.keys()) - set(white_parameters)
            lost_keys = ",".join(list(necessary_keys - receive_keys))
            invalid_keys = ",".join(list(receive_keys - standard_keys))
            legal_keys = receive_keys & standard_keys

            errs = []

            if lost_keys != "":
                errs.append("参数 {} 是必要的".format(lost_keys))

            if invalid_keys != "":
                errs.append("参数 {} 是无效的".format(invalid_keys))

            def core_func():
                if lost_keys or invalid_keys:
                    raise NotImplementedError(";".join(errs))

                for key, key_type in key_type_map.items():
                    # 强制类型转换receive_kwargs字典
                    if key in legal_keys:
                        try:
                            receive_kwargs[key] = transfer_value_type(value=receive_kwargs[key],
                                                                      trans_type=key_type)
                        except Exception as transfer_err:
                            raise Exception(
                                "The key: `{}` transfer from `{}` "
                                "to `{}` get error: {}".format(key,
                                                               type(key),
                                                               key_type,
                                                               str(transfer_err)))

                process_data_func_kwargs = {}
                for key in legal_keys:
                    # 使用二者交集，不能传递非法参数给ORM处理函数
                    process_data_func_kwargs[key] = receive_kwargs[key]

                ret['data'] = process_data_func(**process_data_func_kwargs)

                # 标记访问记录
                record = RequestRecord.objects.filter(
                    method=process_data_func.__name__
                ).latest("time")
                record.kwargs = json.dumps(origin_kwargs)
                record.returns = json.dumps(ret['data'])
                record.save()

            if api_internal_debug:
                core_func()
                status = 200
            else:
                try:
                    core_func()
                    status = 200
                except Exception as e:
                    ret['err_msg'] = str(e)
                    status = 400

            return Response(data=ret, status=status)

        return wrapper

    return decorator
