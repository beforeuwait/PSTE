# coding=utf-8

import json
import time
import logging
import config as cnf
from redis import StrictRedis
from lxml import etree


# logging
logger = logging.getLogger(name='son')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('./pste_log.log')
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt)
logger.addHandler(handler)


def loads_json(js_ctx):
    js_dict = None
    try:
        js_dict = json.loads(js_ctx)
    except Exception as e:
        logger.warning('json解析错误\t{0}, \t{1}'.format(e, js_ctx))

    return js_dict


def json_dumps(json_dict):
    js_ctx = None
    try:
        js_ctx = json.dumps(json_dict)
    except Exception as e:
        logger.warning('json dumps错误\t{0}'.format(e))
    return js_ctx

def load_selector(html):
    selector = None
    try:
        selector = etree.HTML(html)
    except Exception as e:
        logger.warning('xpath解析错误\t{0}'.format(e))
    return selector

# redis

def connect_2_redis():
    cli = None
    try:
        cli = StrictRedis(host=cnf.redis_cnf.get('host'), port=cnf.redis_cnf.get('port'), db=cnf.redis_cnf.get('db'))
    except Exception as e:
        logger.warning('redis链接出错'.format(e))
    return cli


def pop_msg(que):
    msg = None
    redis_cli = connect_2_redis()
    if redis_cli is not None:
        while True:
            if redis_cli.exists(que):
                msg = redis_cli.lpop(que)
                break
            time.sleep(0.1)
    return msg


