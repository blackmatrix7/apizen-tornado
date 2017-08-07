# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/1/4 10:59
# Author: Matrix
# Site:
# File: manage.py
# Software: PyCharm
import time
import signal
import socket
import logging
import tornado.web
import tornado.ioloop
from tookit.router import Route
from apizen import ApiZenManager
from config import current_config
from tookit.cmdline import cmdline
from bootloader import torconf, cache
from tornado.httpserver import HTTPServer
from tookit.session import MemcacheSessionStore
from tornado.options import define, parse_command_line, options

# 定义tornado options
define('cmd', default='runserver', metavar='runserver|syncdb|syncnewdb')
define('port', default=current_config.get('PORT', 8011), type=int)


# ApiZen初始化
apizen = ApiZenManager.init_app(config=current_config)


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

    logging_root = logging.getLogger('root')
    application = Application()
    application.listen(8013)
    tornado.ioloop.IOLoop.instance().start()

    logging_root.info('Server running on http://%s:%s' % ('127.0.0.1', options.port))

if __name__ == '__main__':
    logger_root = logging.getLogger('root')
    logger_root.info("start run web server.")

    parse_command_line()

    if cmdline.command == 'runserver':
        runserver()
    elif cmdline.command == 'runcelery':
        from runcelery import app
        app.start(argv=['celery', 'worker', '-l', 'info'])
