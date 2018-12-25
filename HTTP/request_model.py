# coding=utf-8

"""
请求模块

重写的目的是，增加灵活，减少引用时的重写

"""
import time
import chardet
import HTTP.config as config
import requests
from copy import deepcopy
from HTTP.session_handler import SessionHandler
from HTTP.utils import logger
from HTTP.utils import filter_dict

# type
_html = str
_status_code = int
_switcher = dict
_is_go_on = bool
_resp = tuple


class DealRequest:

    def __init__(self):
        self.session = requests.session()
        self.sh = SessionHandler(self.session)

    # def do_GET(self, *args) -> (_html, _status_code):
    def do_GET(self, *args) -> _resp:
        """完成get请求"""
        html = 'null_html'
        status_code = 0
        try:
            response = self.session.get(url=args[0], params=args[1], allow_redirects=args[3], timeout=30)
        except Exception as e:
            logger.warning('请求出错\t{0}'.format(e, extra=filter_dict))
        else:
            # 请求成功
            status_code = response.status_code
            logger.debug('GET:\t{0}\t{1}'.format(status_code, args[0]))
            # 应该直接返回字节流，不要解码
            html = response.content

        return (html, status_code)
    
    # def do_POST(self, *args) -> (_html, _status_code):
    def do_POST(self, *args) -> _resp:
        """完成POST请求"""
        html = 'null_html'
        status_code = 0
        try:
            response = self.session.post(url=args[0], data=args[2], allow_redirects=args[3], timeout=30)
        except Exception as e:
            logger.warning('请求出错\t{0}'.format(e, extra=filter_dict))
        else:
            # 请求成功
            status_code = response.status_code
            logger.debug('POST:\t{0}\t{1}'.format(status_code, args[0]))
            # 拿到编码
            html = response.content
        
        return (html, status_code)

    def switcher(self) -> _switcher:
        """返回一个选择器"""
        return {'GET': self.do_GET,
                'POST': self.do_POST}

    def do_request(self, method, url, headers, cookies, params, payloads, redirect) -> (_html, _status_code):
        """接受参数，完成请求"""
        # RETRY
        retry = deepcopy(config.retry)
        html = 'null_html'
        status_code = 0
        # 请求放大写
        method = method.upper()
        # 组织部分
        # 更新请求头
        self.sh.update_cookie_headers_params('headers', headers)
        # 更新cookie
        if cookies:
            self.sh.update_cookie_headers_params('cookies', cookies)
        # 执行请求
        while retry > 0:
            html, status_code = self.switcher().get(method)(url, params, payloads, redirect)
            is_go_on = self.deal_response(status_code)
            if status_code != 0 and is_go_on:
                break
            # 说明刚刚的请求失败
            # 这里可以休息一下，再次访问
            time.sleep(config.w_sleep)
            retry -= 1

        return html, status_code

    @staticmethod
    def deal_response(status_code) -> _is_go_on:
        """为了方便重写
        往后只需要重构此部分
        针对 302的情况
        针对 301的情况
        针对 400 + 的情况
        针对 500 + 的情况
        """
        is_go_on = False
        # todo: 这里需要重写.........
        # 不能简单的去设定 status_code 小于300就通过
        # 这几天遇到 521 的情况
        if status_code < 300:
            # 请求通过
            is_go_on = True
        return is_go_on
