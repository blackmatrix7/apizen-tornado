#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/16 上午11:20
# @Author  : Matrix
# @Site    : 
# @File    : handler.py
# @Software: PyCharm
import json
from config import current_config
from decimal import Decimal
from tornado.escape import utf8
from datetime import datetime, date
from tornado.util import unicode_type
from tornado.web import RequestHandler

__author__ = 'blackmatrix'


class CustomJSONEncoder(json.JSONEncoder):

    datetime_format = None

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime(current_config.get('DATETIME_FMT'))
            elif isinstance(obj, date):
                return obj.strftime(current_config.get('DATE_FMT'))
            elif isinstance(obj, Decimal):
                # 不转换为float是为了防止精度丢失
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return json.JSONEncoder.default(self, obj)


class BaseHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def set_default_headers(self):
        pass


class SysBaseHandler(BaseHandler):
    pass


class ApiBaseHandler(SysBaseHandler):

    def __init__(self, application, request, **kwargs):
        self._access_token = None
        self._method = None
        self._app_key = None
        self._sign = None
        self._timestamp = None
        self._v = None
        self._format = 'json'
        SysBaseHandler.__init__(self, application, request, **kwargs)

    def write(self, chunk):
        """Writes the given chunk to the output buffer.

        To write the output to the network, use the flush() method below.

        If the given chunk is a dictionary, we write it as JSON and set
        the Content-Type of the response to be ``application/json``.
        (if you want to send JSON as a different ``Content-Type``, call
        set_header *after* calling write()).

        Note that lists are not converted to JSON because of a potential
        cross-site security vulnerability.  All JSON output should be
        wrapped in a dictionary.  More details at
        http://haacked.com/archive/2009/06/25/json-hijacking.aspx/ and
        https://github.com/facebook/tornado/issues/1009
        """
        if self._finished:
            raise RuntimeError("Cannot write() after finish()")
        if not isinstance(chunk, (bytes, unicode_type, dict)):
            message = "write() only accepts bytes, unicode, and dict objects"
            if isinstance(chunk, list):
                message += ". Lists not accepted for security reasons; see http://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler.write"
            raise TypeError(message)
        if isinstance(chunk, dict):
            chunk = json.dumps(chunk, cls=CustomJSONEncoder).replace("</", "<\\/")
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        chunk = utf8(chunk)
        self._write_buffer.append(chunk)

    def check_xsrf_cookie(self):
        pass


if __name__ == '__main__':
    pass
