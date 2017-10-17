#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 下午3:29
# @Author  : Matrix
# @Site    :
# @File    : routing.py
# @Software: PyCharm
import json
import logging
import tornado.gen
import tornado.web
from manage import celery
from toolkit.router import route
from apizen.manager import async
from json import JSONDecodeError
from config import current_config
from apizen.schema import convert
from apizen.method import get_method
from inspect import Parameter, signature
from webapi.handler import ApiBaseHandler
from tornado.web import MissingArgumentError
from apizen import ApiSysExceptions, SysException

__author__ = 'matrix'


@route(r'/api/router/rest')
@route(r'/api/router/json')
class WebApiRoute(ApiBaseHandler):

    @staticmethod
    @celery.task
    def async_webapi(method, v, args, http_method):

        api_code = 1000
        api_msg = '执行成功'
        http_code = 200
        err_type = None

        try:
            # 获取接口处理函数，及接口部分配置
            api_func = get_method(version=v, api_method=method, http_method=http_method)

            # 最终传递给接口处理方法的全部参数
            func_args = {}

            api_method_params = signature(api_func).parameters
            for k, v in api_method_params.items():
                if str(v.kind) == 'VAR_POSITIONAL':
                    raise ApiSysExceptions.error_api_config
                elif str(v.kind) in ('POSITIONAL_OR_KEYWORD', 'KEYWORD_ONLY'):
                    if k not in args:
                        if v.default is Parameter.empty:
                            missing_arguments = ApiSysExceptions.missing_arguments
                            missing_arguments.err_msg = '{0}：{1}'.format(missing_arguments.err_msg, k)
                            raise missing_arguments
                        func_args[k] = convert(k, v.default, v.default, v.annotation)
                    else:
                        func_args[k] = convert(k, args.get(k), v.default, v.annotation)
                elif str(v.kind) == 'VAR_KEYWORD':
                    func_args.update({k: v for k, v in args.items()
                                      if k not in api_method_params.keys()})
            result = api_func(**func_args)
        except SysException as ex:
            api_code = ex.err_code
            api_msg = ex.err_msg
            http_code = ex.http_code
            err_type = ex.err_type
            result = None
        except BaseException as ex:
            if current_config.DEBUG and current_config.ASYNC is False:
                raise ex
            ex = ApiSysExceptions.system_error
            api_code = ex.err_code
            api_msg = ex.err_msg
            http_code = ex.http_code
            err_type = ex.err_type
            result = None
        return result, api_code, api_msg, http_code, err_type

    def get(self):
        self.handler()

    def post(self):
        self.handler()

    def prepare(self):
        # 接口名称
        self._method = self.get_argument('method')
        # 接口版本
        self._v = self.get_argument('v')
        # 数据格式
        self._format = self.get_argument('format', 'json').lower()

        # 检查请求的格式
        if self._format not in ('json', 'xml'):
            raise ApiSysExceptions.invalid_format

        # 拼装请求参数
        self.content_type = self.request.headers['Content-Type'].lower() if 'Content-Type' in self.request.headers else None
        self.request_args = {key: self.get_argument(key) for key in self.request.arguments}

        if self.request.method == 'POST':

            if self.content_type is None:
                raise ApiSysExceptions.missing_content_type

            if 'application/json' not in self.content_type and 'application/x-www-form-urlencoded' not in self.content_type:
                raise ApiSysExceptions.unacceptable_content_type

            if 'application/json' in self.content_type:
                body_data = json.loads(self.request.body.decode('utf-8'))
                if body_data and isinstance(body_data, dict):
                    self.request_args.update(body_data)
                else:
                    raise ApiSysExceptions.invalid_json

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def handler(self):
        if current_config.ASYNC is True:
            retdata = yield async(self.async_webapi, method=self._method, v=self._v, http_method=self.request.method,
                                  args=self.request_args)
        else:
            retdata = self.async_webapi(method=self._method, v=self._v, http_method=self.request.method, args=self.request_args)

        if isinstance(retdata, BaseException):
            raise retdata
        self.result, self.api_code, self.api_msg, self.http_code, self.err_type = retdata

        if self.api_code != 1000:
            raise SysException(err_code=self.api_code, err_msg=self.api_msg, http_code=self.http_code, err_type=self.err_type)
        else:
            resp = {
                'meta': {
                    'code': self.api_code,
                    'message': self.api_msg
                },
                'response': self.result
            }
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_status(status_code=self.http_code)
            self.write(resp)
        self.on_finish()

    def write_error(self, status_code, **kwargs):
        error_type, error, traceback = kwargs['exc_info']

        # 参数缺失异常
        if isinstance(error, MissingArgumentError):
            # 缺少方法名
            if error.arg_name == 'method':
                _api_ex = ApiSysExceptions.missing_method
            # 缺少版本号
            elif error.arg_name == 'v':
                _api_ex = ApiSysExceptions.missing_version
            # 其他缺少参数的情况
            else:
                _api_ex = ApiSysExceptions.missing_arguments
            self.api_msg = '{0}:{1}'.format(_api_ex.err_msg, error.arg_name)
            self.api_code = _api_ex.err_code
            self.http_code = _api_ex.http_code
        # JSON解析异常
        elif isinstance(error, JSONDecodeError):
            _api_ex = ApiSysExceptions.invalid_json
            self.api_code = _api_ex.err_code
            self.http_code = _api_ex.http_code
            self.api_msg = _api_ex.err_msg
        # API其他异常
        elif isinstance(error, SysException):
            self.api_code = error.err_code
            self.http_code = error.http_code
            self.api_msg = error.err_msg
        # 全局异常
        else:
            # debug 模式，并且没有启用celery实现异步时，直接抛出异常，便于调试
            if current_config.DEBUG and current_config.ASYNC is False:
                raise error
            else:
                _api_ex = ApiSysExceptions.system_error()
                self.api_code = _api_ex.err_code
                self.http_code = _api_ex.http_code
                self.api_msg = '{0}：{1}'.format(_api_ex.err_msg, error) \
                    if current_config.TESTING else _api_ex.err_msg

        retinfo = {
            'meta': {
                'code': self.api_code,
                'message': self.api_msg
            },
            'response': None
        }

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_status(status_code=self.http_code)
        self.write(retinfo)

    def on_finish(self):
        if self.api_code != 1000:
            logging.error(self.resp)

