# !/usr/bin/env python
# coding=utf8

from tornado.web import url
from functools import reduce


class Route(object):

    _routes = {}

    def __init__(self, pattern, kwargs=None, name=None, host='.*$'):
        self.pattern = pattern
        self.kwargs = kwargs if kwargs else {}
        self.name = name
        self.host = host

    def __call__(self, handler_class):
        spec = url(self.pattern, handler_class, self.kwargs, name=self.name)
        self._routes.setdefault(self.host, []).append(spec)
        return handler_class

    @classmethod
    def routes(cls, application=None):
        if application:
            for host, handlers in cls._routes.items():
                application.add_handlers(host, handlers)
        else:
            return reduce(lambda x, y: x+y, cls._routes.values()) if cls._routes else []

route = Route

