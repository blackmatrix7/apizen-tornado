#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/8/5 13:34
# @Author  : BlackMatrix
# @Site : 
# @File : runcelery.py
# @Software: PyCharm
import config
from celery import Celery

__author__ = 'blackmatrix'

config = config.current_config

print(config.CELERY_BROKER_URL)

app = Celery('apizen',  broker=config.CELERY_BROKER_URL)

app.config_from_object('config.current_config')
