#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/6/7 下午9:50
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: controller.py
# @Software: PyCharm
from functools import wraps
from apizen.method import apiconfig
from errors import ApiSubExceptions
from apizen.schema import Integer, String, Float, Dict, DateTime, Email, List, Bool, Date, Money

__author__ = 'blackmatix'


def test_decorator(func):
    """
    装饰器，测试使用，无功能
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@apiconfig(allow_anonymous=True)
def first_api():
    return '这是第一个Api例子'


@apiconfig(allow_anonymous=True)
def register_user(name, age, email=None):
    """
    测试装饰器对获取函数参数的影响，及接口参数判断说明
    :param age:  年龄，必填，原因同上
    :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
    :param email:  电子邮箱
    :return:  返回测试结果
    """
    return {'name': name, 'age': age, 'email': email}


@apiconfig(allow_anonymous=True)
def register_user_plus(name: String, age: Integer, birthday: Date, email=None):
    """
    测试装饰器对获取函数参数的影响，及接口参数判断说明
    :param age:  年龄，必填，原因同上
    :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
    :param birthday:  生日
    :param email:  电子邮箱
    :return:  返回测试结果
    """
    return {'name': name, 'age': age, 'birthday': birthday, 'email': email}


@apiconfig(allow_anonymous=True)
@test_decorator
def validate_email(name: String, age: Integer, birthday: Date, email: Email):
    """
    测试装饰器对获取函数参数的影响，及接口参数判断说明
    :param age:  年龄，必填，原因同上
    :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
    :param birthday:  生日
    :param email:  电子邮箱
    :return:  返回测试结果
    """
    return {'name': name, 'age': age, 'birthday': birthday, 'email': email}


@apiconfig(allow_anonymous=True)
def custom_date_fmt(name: String, age: Integer, birthday: Date('%Y年%M月%d日'), email: Email):
    """
    测试自定义日期格式
    :param age:  年龄，必填，原因同上
    :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
    :param birthday:  生日
    :param email:  电子邮箱
    :return:  返回测试结果
    """
    return {'name': name, 'age': age, 'birthday': birthday, 'email': email}


@apiconfig(allow_anonymous=True)
def money_to_decimal(money: Money):
    """
    测试自定义的Money类型，会转换成Decimal
    :param money:  金额
    :return:
    """
    return money


@apiconfig(allow_anonymous=True)
def json_to_dict(user: Dict):
    return user


@apiconfig(allow_anonymous=True)
def json_to_list(user: List):
    return user


# 演示抛出异常
@apiconfig(allow_anonymous=True)
def raise_error():
    """
    接口抛出异常的使用说明，抛出异常信息后，会在返回接口的code中显示对应异常的编号，
    同时，返回的http code 也会根据异常配置中的status_code而改变
    :return:  返回异常信息
    """
    raise ApiSubExceptions.unknown_error


# 演示自定义异常信息
@apiconfig(allow_anonymous=True)
def custom_error():
    """
    接口抛出异常的使用说明，抛出异常信息后，会在返回接口的code中显示对应异常的编号，
    同时，返回的http code 也会根据异常配置中的 http_code 而改变
    :return:  返回异常信息
    """
    raise ApiSubExceptions.unknown_error('这是一个自定义异常信息')


# 测试自定义异常信息后，对其他地方调用的影响
@apiconfig(allow_anonymous=True)
def after_custom_error():
    """
    接口抛出异常的使用说明，抛出异常信息后，会在返回接口的code中显示对应异常的编号，
    同时，返回的http code 也会根据异常配置中的 http_code 而改变
    :return:  返回异常信息
    """
    ApiSubExceptions.unknown_error('测试自定义异常信息后，对其他地方调用的影响')
    raise ApiSubExceptions.unknown_error


# 保留原始返回格式
@apiconfig(raw_resp=True, allow_anonymous=True)
def raw_data():
    return {'id': 1, 'message': '保留原始返回格式'}


# 不允许匿名访问
def not_allowed_anonymous():
    pass


@apiconfig(allow_anonymous=True)
def is_bool(value: Bool):
    """
    测试布尔值类型
    :param value:
    :return:
    """
    return value


@apiconfig(allow_anonymous=True)
def sleep_seconds(seconds=10):
    import time
    time.sleep(seconds)


@apiconfig(allow_anonymous=True)
def raise_runtime_error():
    raise RuntimeError


@apiconfig(allow_anonymous=True)
def new_article(title, content):
    from .models import Article
    article = Article()
    article.title = title
    article.content = content
    article.insert().commit()
    return article.to_dict()


@apiconfig(allow_anonymous=True)
def new_logs(name, remark):
    from .models import Logs
    logs = Logs()
    logs.name = name
    logs.remark = remark
    logs.insert().commit()
    return logs.to_dict()


@apiconfig(allow_anonymous=True)
def get_articles():
    """
    测试获取全部数据
    :return:
    """
    from .models import Article
    articles = Article.get_all()
    return [article.to_dict() for article in articles]


class ApiDemo:

    def __init__(self):
        self.value = None

    @staticmethod
    @apiconfig(allow_anonymous=True)
    @test_decorator
    def set_user(user_id: Integer, name: String, createtime: DateTime, mark: Float=None, age: Integer=19):
        """
        测试装饰器对获取函数参数的影响，及接口参数判断说明
        :param user_id:  用户id，必填，当函数参数没有默认值时，接口认为是必填参数
        :param age:  年龄，必填，原因同上
        :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
        :param mark:  分数
        :param createtime:  创建日期
        :return:  返回测试结果
        """
        return [
            {'user_id': user_id,  'name': name, 'age': age, 'mark': mark, 'year': createtime.year}
        ]

    # 演示静态方法调用
    @staticmethod
    @apiconfig(allow_anonymous=True)
    def set_users(users: list):
        def return_users():
            for user in users:
                yield {'user_id': user.get('user_id'),
                       'name': user.get('name'),
                       'age': user.get('age')}
        return list(return_users())

    # 演示类方法调用
    @classmethod
    @apiconfig(allow_anonymous=True)
    def class_method(cls, name):
        """
        类方法调用测试
        :param name:  姓名，
        :return:  返回测试结果
        """
        return {'name': name}

    # 演示实例方法调用
    @apiconfig(allow_anonymous=True)
    def instance_func(self, value):
        """
        实例方法调用测试
        :param value:  必填，任意字符串
        :return:  返回测试结果
        """
        self.value = value
        return self.value

    # 演示错误的函数写法
    @staticmethod
    @apiconfig(allow_anonymous=True)
    def err_func(self):
        """
        模拟错误的函数写法：声明为静态方法，却还存在参数self
        此时获取函数签名时，会将self作为一个接口的默认参数，如果不传入值会抛出异常
        :param self: 静态方法的参数，没有默认值，必填，不是实例方法的self参数
        :return:  返回self的值
        """
        return self

    # 演示接口接收任意k/w参数
    @staticmethod
    @apiconfig(allow_anonymous=True)
    def send_kwargs(value: str, **kwargs):
        """
        VAR_KEYWORD 参数类型的传值测试，传入任意k/w，会在调用结果中返回
        :param value:  任意字符串
        :param kwargs:  键值对
        :return:  返回调用结果
        """
        return {"value": value, "kwargs": kwargs}

    # json 转 dict
    @staticmethod
    @apiconfig(allow_anonymous=True)
    def json_to_dict(user: Dict):
        return user

demo = ApiDemo()

if __name__ == '__main__':
    pass
