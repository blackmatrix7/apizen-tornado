# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/1/4 10:59
# Author: Vcan
# Site:
# File: manage.py
# Software: PyCharm
import logging
import tornado.web
from tookit.router import Route
from config import current_config
from tornado.ioloop import IOLoop
from tookit.cmdline import cmdline
from bootloader import cache, torconf
from apizen.manager import ApiZenManager
from tornado.httpserver import HTTPServer
from tookit.session import MemcacheSessionStore
from tornado.options import define, parse_command_line, options

# 定义tornado options
define('cmd', default='runserver', metavar='runserver|syncdb|syncnewdb')
define('port', default=current_config.get('PORT', 8011), type=int)


# ApiZen初始化
apizen = ApiZenManager(config=current_config)


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
    http_server = HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    loop = IOLoop.instance()
    logging_root.info('Server running on http://%s:%s' % ('127.0.0.1', options.port))
    loop.start()

if __name__ == '__main__':
    logger_root = logging.getLogger('root')
    logger_root.info("start run web server.")

    parse_command_line()

    if cmdline.command == 'runserver':
        runserver()
    elif cmdline.command == 'runcelery':
        from runcelery import app
        app.start(argv=['celery', 'worker', '-l', 'info'])
    elif cmdline.command == 'flower':
        from runcelery import app
        app.start(argv=['celery', 'flower', '-l', 'debug'])
    elif cmdline.command == 'delcaches':
        cache.flush_all()
