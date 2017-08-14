#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/12 下午9:46
# @Author  : Matrix
# @Site    : 
# @File    : exception.py
# @Software: PyCharm
from apizen import SysException


# API 子系统（业务）层级执行结果，以2000开始
class ApiSubExceptions:
    empty_result = SysException(err_code=2000, http_code=200, err_msg='查询结果为空', err_type=Exception)
    unknown_error = SysException(err_code=2001, http_code=500, err_msg='未知异常', err_type=Exception)
    other_error = SysException(err_code=2002, http_code=500, err_msg='其它异常', err_type=Exception)

if __name__ == '__main__':
    pass
