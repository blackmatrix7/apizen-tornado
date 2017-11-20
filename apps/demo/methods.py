#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/11/8 下午1:52
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : methods.py
# @Software: PyCharm
from .handlers import *
from apizen.version import ApiMethodsBase

__author__ = 'blackmatrix'


class DemoApiMethods(ApiMethodsBase):
    api_methods = {
        # 第一个API
        'matrix.api.first-api': {'func': first_api},
        # 接口参数自动判断
        'matrix.api.register_user': {'func': register_user},
        # 接口参数类型自动判断
        'matrix.api.register_user_plus': {'func': register_user_plus},
        # 自定义类型判断方式
        'matrix.api.validate_email': {'func': validate_email},
        # 自定义日期格式
        'matrix.api.custom_date_fmt': {'func': custom_date_fmt},
        # 自定义Money类型
        'matrix.api.money_to_decimal': {'func': money_to_decimal},
        # JSON 转 Dict
        'matrix.api.json-to-dict': {'func': json_to_dict},
        # JSON 转 List
        'matrix.api.json-to-list': {'func': json_to_list},
        # 抛出一个异常
        'matrix.api.return-err': {'func': raise_error},
        # 自定义一个异常信息
        'matrix.api.custom-error': {'func': custom_error},
        # 自定义一个异常信息
        'matrix.api.after-custom-error': {'func': after_custom_error},
        # 保留原始返回格式
        'matrix.api.raw_response': {'func': raw_data},
        # 不允许匿名访问
        'matrix.api.not_allowed_anonymous': {'func': not_allowed_anonymous},
        # 只允许GET请求
        'matrix.api.only-get': {'func': first_api, 'methods': ['get']},
        # 只允许POST请求
        'matrix.api.only-post': {'func': first_api, 'methods': ['post']},
        # 允许post和get
        'matrix.api.get-post': {'func': first_api},
        # 停用API
        'matrix.api.api-stop': {'func': first_api, 'enable': False},
        # 布尔值类型
        'matrix.api.is-bool': {'func': is_bool},
        # 错误的函数编写
        'matrix.api.err-func': {'func': demo.err_func},
        # 实例方法调用
        'matrix.api.instance-func': {'func': demo.instance_func},
        # 类方法调用
        'matrix.api.class-func': {'func': demo.class_method},
        # 传递任意参数
        'matrix.api.send-kwargs': {'func': demo.send_kwargs},
        # API版本继承
        'matrix.api.raise-error': {'func': raise_error},
        # 模拟接口阻塞
        'matrix.api.sleep': {'func': sleep_seconds},
        # 模拟接口阻塞
        'matrix.api.runtime-error': {'func': raise_runtime_error},
        # 测试新增文章
        'matrix.demo.articles.set': {'func': new_article},
        # 测试新增文件
        'matrix.demo.logs.set': {'func': new_logs},
        # 测试获取全部数据
        'matrix.demo.articles.get': {'func': get_articles}
    }

if __name__ == '__main__':
    pass
