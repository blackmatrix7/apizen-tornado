#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/8 下午11:12
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: config.py
# @Software: PyCharm
import os
from toolkit.cmdline import cmdline
from apizen.config import BaseConfig
__author__ = 'blackmatrix'


class CommonConfig(BaseConfig):

    DEBUG = True
    TESTING = True
    ASYNC = False

    HOST = '127.0.0.1'
    PORT = 8011

    SITE_NAME = 'ApiZen'
    LOGGER_NAME = 'ApiZenLogger'

    # cookie
    COOKIE_SECRET = '@r3K8mktcn*j5T#^M@qWZJ&tVy!9Spjz'

    # login匹配
    LOGIN_URL = '/signin'

    # 数据库配置

    # ApiZen配置
    APIZEN_ROUTE = ('/api/router/rest', '/api/router/json')
    APIZEN_VERSIONS = ('webapi.methods', )
    APIZEN_DATE_FMT = '%Y-%m-%d'
    APIZEN_DATETIME_FMT = '%Y/%m/%d %H:%M:%S'
    APIZEN_RESP_FMT = '{"meta": {"code": {code}, "message": {message}}, "response": {response}}'

    # 日期格式配置
    DATE_FMT = '%Y-%m-%d'
    DATETIME_FMT = '%Y-%m-%d %H:%M:%S'

    # RabbitMQ
    RabbitMQ_HOST = None
    RabbitMQ_PORT = None
    RabbitMQ_USER = None
    RabbitMQ_PASS = None

    # Cache
    CACHE_MEMCACHED_SERVERS = ['127.0.0.1:11211']
    CACHE_KEY_PREFIX = 'default'

    # Celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
    CELERY_ACCEPT_CONTENT = ['json', 'pickle']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'pickle'
    CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    CELERY_IMPORTS = ('webapi.tasks', 'webapi.methods')
    # celery worker 的并发数
    CELERYD_CONCURRENCY = 3
    # 默认队列
    CELERY_DEFAULT_QUEUE = 'celery@apizen.default'


# 开发环境配置
class DevConfig(CommonConfig):

    DEBUG = True
    TESTING = False
    ASYNC = False

    # Cache
    CACHE_KEY_PREFIX = 'debug'

    # Port
    PORT = 8011


# 测试环境配置
class TestConfig(CommonConfig):

    DEBUG = False
    TESTING = True
    ASYNC = False

    # Cache
    CACHE_KEY_PREFIX = 'test'

    # Port
    PORT = 8012


# 生产环境配置
class ProdConfig(CommonConfig):

    DEBUG = False
    TESTING = False
    ASYNC = True

    # Cache
    CACHE_KEY_PREFIX = 'master'
    # 默认队列
    CELERY_DEFAULT_QUEUE = 'celery@apizen.prod'

    # Port
    PORT = 8013

devcfg = DevConfig()
testcfg = TestConfig()
prodcfg = ProdConfig()
default = devcfg

configs = {
    'devcfg': devcfg,
    'testcfg': testcfg,
    'prodcfg': prodcfg,
    'default': devcfg
}

config_name = cmdline.config
try:
    import localconfig
    current_config = localconfig.configs[config_name]
except ImportError:
    current_config = configs[config_name]
