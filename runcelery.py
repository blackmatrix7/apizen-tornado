#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/8/5 13:34
# @Author  : BlackMatrix
# @Site : 
# @File : runcelery.py
# @Software: PyCharm
from config import current_config
from celery import Celery

__author__ = 'blackmatrix'

app = Celery('apizen', broker=current_config.CELERY_BROKER_URL)

app.config_from_object('config.config')
