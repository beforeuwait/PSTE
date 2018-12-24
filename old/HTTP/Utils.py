# coding=utf8

"""
    定义一些常见的处理
    以及
    自定义异常
"""


def check_params(params):
    """检查参数是否为dict"""
    if not isinstance(params, dict):
        raise InputParamsError


class InputParamsError(Exception):
    
    def __str__(self):
        return '当前传入参数不是dict格式，请检查...'
