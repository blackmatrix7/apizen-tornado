#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/8/9 下午8:02
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: async.py
# @Software: PyCharm
from tornado.ioloop import IOLoop
from tornado.concurrent import Future

__author__ = 'blackmatrix'

ioloop = IOLoop.instance()


def async(task, *args, **kwargs):
    future = Future()
    result = task.delay(*args, **kwargs)
    IOLoop.instance().add_callback(_on_result, result, future)
    return future


def _on_result(result, future):
    # if result is not ready, add callback function to next loop,
    if result.ready():
        future.set_result(result.result)
    else:
        IOLoop.instance().add_callback(_on_result, result, future)


if __name__ == '__main__':
    pass
