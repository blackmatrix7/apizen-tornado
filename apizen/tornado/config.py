#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/7/26 21:41
# @Author  : BlackMatrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : config.py
# @Software: PyCharm
from ..config import CommonConfig
"""
-------------------------------
ApiZen 接口版本的注册、管理与继承功能
-------------------------------
适用版本：Tornado
-------------------------------
其他说明：

ApiZen提供一个默认的接口路由，默认为激活状态。
通过配置文件可以进行关闭。
如果不激活默认接口路由，则以下配置无效：
APIZEN_ROUTE、APIZEN_RESP_FMT
"""

__author__ = 'blackmatrix'

__all__ = ['default_config']


class ConfigMixin:

    def __setitem__(self, key, value):
        raise AttributeError

    def __delitem__(self, key):
        raise AttributeError

    def __getitem__(self, item):
        return getattr(self, item)

    def get(self, item, value=None):
        return getattr(self, item, value)


class DefaultConfig(CommonConfig, ConfigMixin):
    pass


default_config = DefaultConfig()


if __name__ == '__main__':
    pass

