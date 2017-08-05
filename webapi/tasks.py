#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/8/4 22:37
# @Author  : BlackMatrix
# @Site : 
# @File : tasks.py
# @Software: PyCharm
from runcelery import app
__author__ = 'blackmatrix'


@app.task
def add(x, y):
    return x+y

if __name__ == '__main__':
    pass
