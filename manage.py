# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/1/4 10:59
# Author: Vcan
# Site:
# File: manage.py
# Software: PyCharm
import os
import importlib
import tornado.web
from toolkit.router import Route
from config import current_config
from tornado.ioloop import IOLoop
from toolkit.cmdline import cmdline
from apizen.manager import ApiZenManager
from tornado.httpserver import HTTPServer
from extensions import cache, celery, logger
from tornsql.patching import monkey_patching
from toolkit.session import MemcacheSessionStore

# ApiZen初始化
apizen = ApiZenManager(config=current_config)

# 猴子补丁，保证sqlalchemy session 在 tornado 异步况下的安全
monkey_patching()

# 加载Apps
apps = current_config.IMPORT_APPS
try:
    for app in apps:
        importlib.import_module('apps.{0}.models'.format(app))
        importlib.import_module('apps.{0}.methods'.format(app))
        importlib.import_module('apps.{0}.handlers'.format(app))
except ImportError:
        pass

# tornado 配置
torconf = {
        'style_path': os.path.join(os.path.dirname(__file__), 'style'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'upload_path': os.path.join(os.path.dirname(__file__), 'upload'),
        'cookie_secret': current_config.get('COOKIE_SECRET'),
        'login_url': current_config.get('LOGIN_URL'),
        "xsrf_cookies": True,
        'autoescape': None
    }


class Application(tornado.web.Application):
    def __init__(self):

        self.memcachedb = cache

        self.session_store = MemcacheSessionStore(cache)

        handlers = [
                       tornado.web.url(r"/style/(.+)", tornado.web.StaticFileHandler,
                                       dict(path=torconf['style_path']), name='style_path'),
                       tornado.web.url(r"/static/(.+)", tornado.web.StaticFileHandler,
                                       dict(path=torconf['static_path']), name='static_path'),
                       tornado.web.url(r"/upload/(.+)", tornado.web.StaticFileHandler,
                                       dict(path=torconf['upload_path']), name='upload_path')
                   ] + Route.routes()
        tornado.web.Application.__init__(self, handlers, **torconf)


def runserver():
    """
    启动web服务器
    :return:
    """
    logger.info("start run web server.")
    http_server = HTTPServer(Application(), xheaders=True)
    http_server.listen(current_config.PORT)
    loop = IOLoop.instance()
    logger.info('Server running on http://%s:%s' % ('127.0.0.1', current_config.PORT))
    loop.start()


def runcelery():
    """
    启动celery
    :return:
    """
    celery.start(argv=['celery', 'worker', '-l', 'debug' if current_config.DEBUG else 'info', '-f', 'logs/celery.log'])


def runflower():
    """
    启动flower
    :return:
    """
    celery.start(argv=['celery', 'flower', '-l', 'debug' if current_config.DEBUG else 'info', '-f', 'logs/celery.log'])


def delcache():
    """
    清理所有缓存
    :return:
    """
    cache.flush_all()

if __name__ == '__main__':

    logger.info('config name：{}'.format(cmdline.config))

    cmds = {
        # 启动服务器
        'runserver': runserver,
        # 启动celery worker
        'runcelery': runcelery,
        # 启动celery flower
        'runflower': runflower,
        # 清理全部缓存
        'delcache': delcache,
        # 初始化工作流数据库
        'initdb': None
    }.get(cmdline.command, 'runserver')()
