#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/9 下午4:27
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : async.py
# @Software: PyCharm

from tornado.ioloop import IOLoop
from tornado.concurrent import TracebackFuture

__author__ = 'blackmatrix'


def async(task, *args, **kwargs):
    _future = TracebackFuture()
    callback = kwargs.pop("callback", None)
    if callback:
        IOLoop.instance().add_future(_future, lambda future: callback(future.result()))
    result = task.delay(*args, **kwargs)
    IOLoop.instance().add_callback(_on_result, result, _future)
    return _future


def _on_result(result, future):
    # if result is not ready, add callback function to next loop,
    if result.ready():
        future.set_result(result.result)
    else:
        IOLoop.instance().add_callback(_on_result, result, future)
if __name__ == '__main__':
    pass
