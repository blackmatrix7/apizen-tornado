#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/4 上午11:03
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : manager.py
# @Software: PyCharm
import importlib

__author__ = 'blackmatrix'


class ApiZenManager:

    config = None
    celery = None

    @classmethod
    def init_app(cls, config, celery):
        cls.config = config
        cls.celery = celery
        # 导入Api版本
        cls.import_api_versions(versions=config.get('APIZEN_VERSIONS'))
        return cls(config, celery)

    def __init__(self, config, celery):
        self.config = config
        self.celery = celery

    # 导入Api版本
    @staticmethod
    def import_api_versions(versions):
        if versions:
            for version in versions:
                importlib.import_module(version)


if __name__ == '__main__':
    pass
