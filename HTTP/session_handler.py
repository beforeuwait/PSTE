# coding=utf-8

"""
    session 处理

"""

from importlib import reload
import HTTP.config as config
from HTTP.utils import check_params

# type
_check_type = dict
_proxy = config.proxy
_outer_params = dict


class SessionHandler:
    """
    承担对session的操作
    """

    def __init__(self, session) -> None:
        self._s = session
        # 加载proxy
        self.update_proxy()

    def close_session(self) -> None:
        """关闭session"""
        self._s.close()
        return

    def outer_parmams_dict(self) -> _outer_params:
        return {
            'headers': self._s.headers,
            'cookies': self._s.cookies,
            'params': self._s.params
        }

    def update_cookie_headers_params(self, *args) -> None:
        """参数 第一个是说明类型，第二是值"""
        if check_params(_check_type, args[1]):
            self.outer_parmams_dict().get(args[0]).update(args[1])
        return

    def discard_cookie_headers_params(self, choice) -> None:
        """删除session里指定的值"""
        self.outer_parmams_dict().get(choice).clear()
        return

    def update_proxy(self) -> None:
        """这个在默认的状态下是要携带代理的
        可以指定情况，不要代理
        """
        # 对config模块更新
        reload(config)
        self._s.proxies.update(_proxy)
        return

    def discard_proxy(self) -> None:
        """删除session里的proxy
        """
        self._s.proxies.clear()
        return
