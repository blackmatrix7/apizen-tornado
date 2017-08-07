#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/8/5 22:31
# @Author  : BlackMatrix
# @Site : 
# @File : tasks.py
# @Software: PyCharm
from runcelery import app
from inspect import Parameter
from apizen.schema import convert
from apizen.method import get_method
from apizen.exceptions import ApiSysExceptions

__author__ = 'blackmatrix'


@app.task
def async_webapi(method, v, args, http_method):

    # 获取接口处理函数，及接口部分配置
    api_func, sign,  async_api_func, *_ = get_method(version=v, api_method=method, http_method=http_method)

    # 最终传递给接口处理方法的全部参数
    func_args = {}

    api_method_params = sign.parameters
    for k, v in api_method_params.items():
        if str(v.kind) == 'VAR_POSITIONAL':
            raise ApiSysExceptions.error_api_config
        elif str(v.kind) in ('POSITIONAL_OR_KEYWORD', 'KEYWORD_ONLY'):
            if k not in args:
                if v.default is Parameter.empty:
                    missing_arguments = ApiSysExceptions.missing_arguments
                    missing_arguments.err_msg = '{0}：{1}'.format(missing_arguments.err_msg, k)
                    raise missing_arguments
                func_args[k] = convert(k, v.default, v.default, v.annotation)
            else:
                func_args[k] = convert(k, args.get(k), v.default, v.annotation)
        elif str(v.kind) == 'VAR_KEYWORD':
            func_args.update({k: v for k, v in args.items()
                              if k not in api_method_params.keys()})
    result = api_func(**func_args)
    return result
