#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/11/13 下午3:14
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : apps.py
# @Software: PyCharm
import importlib

__author__ = 'blackmatrix'


def import_app_module(app_name, module_name):
    try:
        importlib.import_module('apps.{0}.{1}'.format(app_name, module_name))
    except ImportError:
        pass


def import_apps(apps):
    for app in apps:
        import_app_module(app, 'models')
        import_app_module(app, 'handlers')
        import_app_module(app, 'methods')


if __name__ == '__main__':
    pass
