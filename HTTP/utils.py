# coding=utf-8

import os
import logging

# type
_check_params = bool


def check_params(typeof, ins) -> _check_params:
    """
    检测类型
    :param typeof: 期望类型
    :param ins: 目标
    :return: bool
    """
    result = False
    try:
        if isinstance(ins, typeof):
            return True
    except Exception as e:
        logger.warning('传入的参数格式错误\t{0}\t参数为: {1}'.format(e, ins))
    return result


# logging部分
# 定义个过滤器
class RequestFilter(logging.Filter):
    """这是一个过滤request_log的过滤器
    """

    def filter(self, record):
        result = False
        try:
            filter_key = record.isRequest
        except AttributeError:
            filter_key = 'error_record'

        if filter_key == 'notRequestLog':
            result = True
        return result


logger = logging.getLogger(name='HTTP')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(os.path.join(os.path.split(__file__)[0], './http_log.log'))
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt)
logger.addHandler(handler)

# 添加过滤器
logger.addFilter(RequestFilter())

filter_dict = {"isRequest": "notRequestLog"}


# 定义一个异常

class MethodCheckError(Exception):

    def __str__(self):
        return '当前传入method不是指定的格式类型，参照 get,post'
