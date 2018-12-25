# coding=utf8

"""
外部引用的api
"""

import chardet
from HTTP.request_model import DealRequest
from HTTP.utils import MethodCheckError

# type
_html = str
_status_code = int


class HttpApi:

    def __init__(self) -> None:
        self.dr = DealRequest()

    def receive_and_request(self, **kwargs) -> _html:
        """
        接受参数，这里要检查method
        :param kwargs:
        :return:
        """
        # todo: 添加一个对method的判断，不是 get/post 则报错
        method = kwargs.get('method')
        if method not in ['get', 'GET', 'post', 'POST']:
            raise MethodCheckError
        url = kwargs.get('url')
        headers = kwargs.get('headers')
        cookies = kwargs.get('cookies')
        params = kwargs.get('params')
        payloads = kwargs.get('payloads')
        resp = self.dr.do_request(method=method,
                                              url=url,
                                              headers=headers,
                                              cookies=cookies,
                                              params=params,
                                              payloads=payloads,
                                              redirect=False)
        # 清理headers
        # 清理cookie
        # 关闭session
        page_code = chardet.detect(resp[0]).get('encoding')
        html = resp[0].decode('utf-8') if page_code == 'utf-8' else resp[0].decode('gbk')
        [self.dr.sh.discard_cookie_headers_params(i) for i in ['headers', 'cookies', 'params']]
        self.dr.sh.close_session()
        return html

    def user_define_request(self, **kwargs) -> None:
        """这个方法的意义在于用户自己去设计请求过程
        一般登录啊
        绕过js啊
        。。。
        都这这里自己定义
        """
        pass
