# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/3/14 8:43
# @Author: Matrix
# @Site:
# @File: methods.py
# @Software: PyCharm
from apizen.version import ApiMethodsBase, version
from services.tests.methods import DemoApiMethods

__author__ = 'matrix'


@version(0.9, enable=False)
class ApiMethodsV09(ApiMethodsBase):
    pass


@version(1.0)
class ApiMethodsV10(ApiMethodsBase, DemoApiMethods):
    api_methods = {}


if __name__ == '__main__':
    api_list = ApiMethodsV10.api_methods
    print(api_list)
