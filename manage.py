# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/1/4 10:59
# Author: Vcan
# Site:
# File: manage.py
# Software: PyCharm
import logging
import tornado.web
from toolkit.router import Route
from config import current_config
from tornado.ioloop import IOLoop
from toolkit.cmdline import cmdline
from bootloader import cache, torconf
from apizen.manager import ApiZenManager
from tornado.httpserver import HTTPServer
from toolkit.session import MemcacheSessionStore

# ApiZen初始化
apizen = ApiZenManager(config=current_config)

logger_root = logging.getLogger('root')


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
    logger_root.info("start run web server.")
    http_server = HTTPServer(Application(), xheaders=True)
    http_server.listen(current_config.PORT)
    loop = IOLoop.instance()
    logger_root.info('Server running on http://%s:%s' % ('127.0.0.1', current_config.PORT))
    loop.start()


def runcelery():
    """
    启动celery
    :return:
    """
    from runcelery import app
    app.start(argv=['celery', 'worker', '-l', 'debug' if current_config.DEBUG else 'info', '-f', 'logs/celery.log'])


def runflower():
    """
    启动flower
    :return:
    """
    from runcelery import app
    app.start(argv=['celery', 'flower', '-l', 'debug' if current_config.DEBUG else 'info'])


def delcache():
    """
    清理所有缓存
    :return:
    """
    cache.flush_all()

if __name__ == '__main__':

    logger_root.info('当前配置文件：{}'.format(cmdline.config))

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
