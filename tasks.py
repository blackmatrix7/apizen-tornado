#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/8/4 22:37
# @Author  : BlackMatrix
# @Site : 
# @File : tasks.py
# @Software: PyCharm
from runcelery import app
from apizen.method import run_method
__author__ = 'blackmatrix'


@app.task
def add(x, y):
    return x+y


@app.task
def async_run_method(api_method, request_params):
    return run_method(api_method, request_params)


if __name__ == '__main__':
    pass
