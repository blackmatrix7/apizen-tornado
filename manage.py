# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2017/1/4 10:59
# Author: Vcan
# Site:
# File: manage.py
# Software: PyCharm
import os
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
from toolkit.apps import import_apps, apps_static_path

# ApiZen初始化
apizen = ApiZenManager(config=current_config)

# 猴子补丁，保证sqlalchemy session 在 tornado 异步况下的安全
monkey_patching()

# 加载Apps
import_apps(current_config.IMPORT_APPS)

# tornado 配置
# 基础静态目录
static_paths = {
    'style': os.path.abspath('style'),
    'static': os.path.abspath('static'),
    'upload': os.path.abspath('upload'),
}
# APP加载的静态目录
static_paths.update(apps_static_path(current_config.IMPORT_APPS))
# 其他tornado配置
torconf = {
    'cookie_secret': current_config.get('COOKIE_SECRET'),
    'login_url': current_config.get('LOGIN_URL'),
    "xsrf_cookies": current_config.get('XSRF', True),
    'autoescape': None
}


class Application(tornado.web.Application):
    def __init__(self):

        self.memcachedb = cache

        self.session_store = MemcacheSessionStore(cache)

        handlers = [
            tornado.web.url('/{}/(.+)'.format(k), tornado.web.StaticFileHandler,
                            {'path': static_paths[k]}, name=k) for k, v in static_paths.items()] + Route.routes()

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


def initdb():
    print('请输入 yes 确认重置数据库')
    result = input().lower()
    if result == 'yes':
        from apps.demo.models import Article
        from tornsql.session import DataBaseSQLite
        db = DataBaseSQLite(connect_str=current_config.DEMO_DB_CONNECT)
        db.drop_db()
        db.init_db()
        from apps.demo.models import Logs
        db = DataBaseSQLite(connect_str=current_config.LOGS_DB_CONNECT)
        db.drop_db()
        db.init_db()


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
        'initdb': initdb
    }.get(cmdline.command, 'runserver')()
