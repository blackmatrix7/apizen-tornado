#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/11/9 下午2:34
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : databases.py
# @Software: PyCharm
from config import current_config
from tornsql.session import create_engine, create_db, new_db

__author__ = 'blackmatrix'


engine = create_engine(connect_str=current_config.WORKFLOW_DB_CONNECT)

db = create_db(engine)

new_db('name', db, engine)


if __name__ == '__main__':
    pass
