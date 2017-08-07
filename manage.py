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
from tookit.router import Route
from apizen import ApiZenManager
from config import current_config
from tornado.ioloop import IOLoop
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
    http_server = HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    loop = IOLoop.instance()

    def shutdown():
        logging_root.info('Server stopping ...')
        http_server.stop()
        logging_root.info('IOLoop will be terminate in 1 seconds')
        deadline = time.time() + 1

        def terminate():
            now = time.time()

            if now < deadline and (loop._callbacks or loop._timeouts):
                loop.add_timeout(now + 1, terminate)
            else:
                loop.stop()
                logger_root.info('Server shutdown')

        terminate()

    def sig_handler(sig):
        logging_root.warning('Caught signal:%s', sig)
        loop.add_callback(shutdown)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    ip_list = socket.gethostbyname_ex(socket.gethostname())
    local_ip = ip_list[2][len(ip_list[2]) - 1]
    logging_root.info('Server running on http://%s:%s' % (local_ip, options.port))
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
