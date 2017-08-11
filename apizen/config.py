#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/11 下午4:33
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : config.py
# @Software: PyCharm

__author__ = 'blackmatrix'


try:
    import flask
    from .flask import config as default_config
except ImportError:
    import tornado
    from .tornado import default_config, ConfigMixin

if __name__ == '__main__':
    pass
