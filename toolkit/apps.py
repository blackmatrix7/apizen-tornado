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


def apps_static_path(apps):
    static_paths = {}
    for app in apps:
        app_static_path = 'apps/{}/static'.format(app)
        app_style_path = 'apps/{}/style'.format(app)
        app_upload_path = 'apps/{}/upload'.format(app)
        static_paths.update({'{}/static'.format(app): os.path.abspath(app_static_path)})
        static_paths.update({'{}/style'.format(app): os.path.abspath(app_style_path)})
        static_paths.update({'{}/upload'.format(app): os.path.abspath(app_upload_path)})
    return static_paths


if __name__ == '__main__':
    pass
