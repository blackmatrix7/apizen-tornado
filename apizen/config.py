#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/11 下午4:33
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : config.py
# @Software: PyCharm

__author__ = 'blackmatrix'


class CommonConfig:

    # 是否激活ApiZen默认的路由
    ACTIVATE_DEFAULT_ROUTE = True

    # 接口路由默认地址
    APIZEN_ROUTE = ('/api/router/rest', '/api/router/json')

    # 接口默认返回格式
    APIZEN_RESP_FMT = '{"meta": {"code": {code}, "message": {message}}, "response": {response}}'

    # 接口版本位置
    APIZEN_VERSIONS = None

    # 默认Date格式
    APIZEN_DATE_FMT = '%Y/%m/%d'

    # 默认DateTime格式
    APIZEN_DATETIME_FMT = '%Y/%m/%d %H:%M:%S'


try:
    import flask
    from .flask import config as default_config
except ImportError:
    import tornado
    from .tornado import default_config, ConfigMixin

if __name__ == '__main__':
    pass
