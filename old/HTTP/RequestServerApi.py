# coding=utf8

"""
    author: wangjiawei
    date: 2018/07/09

"""

from HTTP.generalRequest import GeneralRequest

        
class RequestAPI(GeneralRequest):
    """这个类作为外部调用的api
    功能：
    """

    def __init__(self):
        # 实例化GeneralRequest 准备请求
        super(RequestAPI, self).__init__()

    def receive_and_request(self, **kwargs):
        """接收参数
        处理参数
        选择请求方式
        默认是带代理的
        """
        
        # 先获取参数， 目前就想了这么多
        url = kwargs.get('url')
        headers = kwargs.get('headers')
        method = kwargs.get('method')
        cookie = kwargs.get('cookie')
        params = kwargs.get('params')
        payloads = kwargs.get('payloads')
        
        # 构建请求头
        if headers is not None:
            self.update_headers(headers)
        if cookie is not None:
            self.update_cookie_with_outer(cookie)

        # 开始请求
        html = self.do_request(url=url,
                                params=params, 
                                method=method, 
                                payloads=payloads)
        # 在通用的一次性请求里，到这里是要关闭session的
        # 清理cookie
        self.discard_cookies()
        self.close_session()

        return html
    
    def user_define_request(self, **kwargs):
        """这个方法的意义在于用户自己去设计请求过程
        一般登录啊
        绕过js啊
        。。。
        都这这里自己定义
        """
        pass
