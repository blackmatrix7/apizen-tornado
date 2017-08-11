#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/4 上午11:03
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : manager.py
# @Software: PyCharm
import importlib

"""
-------------------------------
ApiZen初始化管理模块
-------------------------------
适用版本：Tornado
"""

__author__ = 'blackmatrix'


class ApiZenManager:

    config = None

    def __init__(self, config=None):
        if config is None:
            ApiZenManager.config = defaultconfig
        else:
            ApiZenManager.config = config
        # 导入Api版本
        self.import_api_versions(versions=ApiZenManager.config.get('APIZEN_VERSIONS'))

    # 导入Api版本
    @staticmethod
    def import_api_versions(versions):
        if versions:
            for version in versions:
                importlib.import_module(version)


if __name__ == '__main__':
    pass
