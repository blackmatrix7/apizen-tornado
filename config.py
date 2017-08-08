#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/8 下午11:12
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: config.py
# @Software: PyCharm
import os
from tookit.cmdline import cmdline

__author__ = 'blackmatrix'


class ConfigMixin:

    def __setitem__(self, key, value):
        raise AttributeError

    def __delitem__(self, key):
        raise AttributeError

    def __getitem__(self, item):
        return getattr(self, item)

    def get(self, item, value=None):
        return getattr(self, item, value)


class BaseConfig(ConfigMixin):

    DEBUG = True
    TESTING = True

    HOST = '127.0.0.1'
    PORT = 8011

    SITE_NAME = 'ApiZen'
    LOGGER_NAME = 'ApiZenLogger'

    # cookie
    COOKIE_SECRET = '@r3K8mktcn*j5T#^M@qWZJ&tVy!9Spjz'

    # login
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
    CELERY_ACCEPT_CONTENT = ['pickle']
    CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'
    CELERY_IMPORTS = ('webapi.tasks', 'webapi.methods')
    # celery worker 的并发数
    CELERYD_CONCURRENCY = 3
    # 默认队列
    CELERY_DEFAULT_QUEUE = 'celery@apizen.default'


# 开发环境配置
class DevConfig(BaseConfig):

    DEBUG = True
    TESTING = True

    # Cache
    CACHE_KEY_PREFIX = 'debug'

    # Port
    PORT = 8011


# 测试环境配置
class TestConfig(BaseConfig):

    DEBUG = False
    TESTING = True

    # Cache
    CACHE_KEY_PREFIX = 'test'

    # Port
    PORT = 8012


# 生产环境配置
class ProdConfig(BaseConfig):

    DEBUG = False
    TESTING = False

    # Cache
    CACHE_KEY_PREFIX = 'master'

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