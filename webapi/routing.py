#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 下午3:29
# @Author  : Matrix
# @Site    :
# @File    : routing.py
# @Software: PyCharm
import json
import tcelery
import logging
import tornado.gen
import tornado.web
from config import current_config
from tookit.router import route
from json import JSONDecodeError
from webapi.handler import ApiBaseHandler
from tornado.web import MissingArgumentError
from apizen.method import get_method
from tasks import async_run_method
from apizen.exceptions import ApiSysExceptions, SysException

__author__ = 'matrix'

tcelery.setup_nonblocking_producer()


@route(r'/api/router/rest')
@route(r'/api/router/json')
class WebApiRoute(ApiBaseHandler):

    def handler(self):

        result = None
        api_code = 1000
        api_msg = '执行成功'
        http_code = 200

        try:
            result = self.call_api_func()
        # 参数缺失异常
        except MissingArgumentError as miss_arg_err:
            # 缺少方法名
            if miss_arg_err.arg_name == 'method':
                api_ex = ApiSysExceptions.missing_method
            # 缺少版本号
            elif miss_arg_err.arg_name == 'v':
                api_ex = ApiSysExceptions.missing_version
            # 其他缺少参数的情况
            else:
                api_ex = ApiSysExceptions.missing_arguments
            api_msg = '{0}:{1}'.format(api_ex.err_msg, miss_arg_err.arg_name)
            api_code = api_ex.err_code
            http_code = api_ex.http_code
        # JSON解析异常
        except JSONDecodeError:
            api_ex = ApiSysExceptions.invalid_json
            api_code = api_ex.err_code
            http_code = api_ex.http_code
            api_msg = api_ex.err_msg
        # API其他异常
        except SysException as api_ex:
            api_code = api_ex.err_code
            http_code = api_ex.http_code
            api_msg = api_ex.err_msg
        # 全局异常
        except Exception as ex:
            if current_config.DEBUG is False:
                api_ex = ApiSysExceptions.system_error
                api_code = api_ex.err_code
                http_code = api_ex.http_code
                api_msg = '{0}：{1}'.format(api_ex.err_msg, ex)
            else:
                raise ex

        retinfo = {
            'meta': {
                'code': api_code,
                'message': api_msg
            },
            'response': result
        }

        if api_code != 1000:
            logging.info(retinfo)

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_status(status_code=http_code)
        self.write(retinfo)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def call_api_func(self):

        resp = None
        api_code = 1000
        api_msg = '执行成功'
        http_code = 200
        try:
            # 接口名称
            self._method = self.get_argument('method')
            # 接口版本
            self._v = self.get_argument('v')
            # 数据格式
            self._format = self.get_argument('format', 'json').lower()
            # access_token
            self._access_token = self.get_argument('access_token', None)
            # app_key
            self._app_key = self.get_argument('app_key', None)
            # 签名
            self._sign = self.get_argument('sign', None)
            # 时间戳
            self._timestamp = self.get_argument('timestamp', None)

            # 检查请求的格式
            if self._format not in ('json', 'xml'):
                raise ApiSysExceptions.invalid_format

            # 拼装请求参数
            content_type = self.request.headers['Content-Type'].lower() if 'Content-Type' in self.request.headers else None
            request_args = {key: self.get_argument(key) for key in self.request.arguments}

            if self.request.method == 'POST':
                if content_type is None:
                    raise ApiSysExceptions.missing_content_type

                if 'application/json' not in content_type and 'application/x-www-form-urlencoded' not in content_type:
                    raise ApiSysExceptions.unacceptable_content_type

                if 'application/json' in content_type:
                    body_data = json.loads(self.request.body.decode())
                    if body_data and isinstance(body_data, dict):
                        request_args.update(body_data)
                    else:
                        raise ApiSysExceptions.invalid_json

            # 获取接口处理函数，及接口部分配置
            api_func, sign,  async_api_func, *_ = get_method(version=self._v, api_method=self._method, http_method=self.request.method)
            # result = async_run_method(api_func, request_params=request_args)

            # 最终传递给接口处理方法的全部参数
            func_args = {}
            # 获取函数方法的参数
            from inspect import Parameter
            from apizen.schema import convert
            api_method_params = sign.parameters

            for k, v in api_method_params.items():
                if str(v.kind) == 'VAR_POSITIONAL':
                    raise ApiSysExceptions.error_api_config
                elif str(v.kind) in ('POSITIONAL_OR_KEYWORD', 'KEYWORD_ONLY'):
                    if k not in request_args:
                        if v.default is Parameter.empty:
                            missing_arguments = ApiSysExceptions.missing_arguments
                            missing_arguments.err_msg = '{0}：{1}'.format(missing_arguments.err_msg, k)
                            raise missing_arguments
                        func_args[k] = convert(k, v.default, v.default, v.annotation)
                    else:
                        func_args[k] = convert(k, request_args.get(k), v.default, v.annotation)
                elif str(v.kind) == 'VAR_KEYWORD':
                    func_args.update({k: v for k, v in request_args.items()
                                      if k not in api_method_params.keys()})

            import tornado.gen
            # return api_method(**func_args)
            result = yield tornado.gen.Task(async_api_func.apply_async, kwargs={**func_args})
            resp = result.result
            if isinstance(resp, Exception):
                raise resp
        # 参数缺失异常
        except MissingArgumentError as miss_arg_err:
            # 缺少方法名
            if miss_arg_err.arg_name == 'method':
                api_ex = ApiSysExceptions.missing_method
            # 缺少版本号
            elif miss_arg_err.arg_name == 'v':
                api_ex = ApiSysExceptions.missing_version
            # 其他缺少参数的情况
            else:
                api_ex = ApiSysExceptions.missing_arguments
            api_msg = '{0}:{1}'.format(api_ex.err_msg, miss_arg_err.arg_name)
            api_code = api_ex.err_code
            http_code = api_ex.http_code
        # JSON解析异常
        except JSONDecodeError:
            api_ex = ApiSysExceptions.invalid_json
            api_code = api_ex.err_code
            http_code = api_ex.http_code
            api_msg = api_ex.err_msg
        # API其他异常
        except SysException as api_ex:
            api_code = api_ex.err_code
            http_code = api_ex.http_code
            api_msg = api_ex.err_msg
        # 全局异常
        except Exception as ex:
            if current_config.DEBUG is False:
                api_ex = ApiSysExceptions.system_error
                api_code = api_ex.err_code
                http_code = api_ex.http_code
                api_msg = '{0}：{1}'.format(api_ex.err_msg, ex)
            else:
                raise ex

        retinfo = {
            'meta': {
                'code': api_code,
                'message': api_msg
            },
            'response': None
        }

        if api_code != 1000:
            logging.info(retinfo)

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_status(status_code=http_code)
        self.write(retinfo)

    def get(self):
        self.call_api_func()

    def post(self):
        self.call_api_func()

    def write_error(self, status_code, **kwargs):
        pass


if __name__ == '__main__':
    pass

