#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/4 上午11:03
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : __init__.py
# @Software: PyCharm
import sys

FLASK = False
TORNADO = False

if 'flask' in sys.modules and 'tornado' not in sys.modules:
    FLASK, TORNADO = True, False
    from .flask.manager import ApiZenManager
elif 'tornado' in sys.modules and 'flask' not in sys.modules:
    FLASK, TORNADO = False, True
    from .tornado.manager import ApiZenManager

__author__ = 'blackmatrix'
