#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/11/8 下午1:53
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : models.py
# @Software: PyCharm
from tornsql.model import ModelBase
from sqlalchemy import Column, String, Text

__author__ = 'blackmatrix'


class Article(ModelBase):

    __tablename__ = 'article'
    __database__ = 'demo'

    title = Column(String(40), nullable=True)
    content = Column(Text, nullable=True)


class Logs(ModelBase):

    __tablename__ = 'logs'
    __database__ = 'logs'

    name = Column(String(40), nullable=True)
    remark = Column(String(40), nullable=True)


if __name__ == '__main__':
    pass
