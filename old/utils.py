# coding=utf8


import time
import os
import json
import config
from config import logger
from lxml import etree
from redis import StrictRedis


# 重复执行次数

def do_fun_cycle(fun, count):
    """重复执行函数"""
    n = 0
    while n < count:
        fun()
        n += 1
    return

def do_fun_cycle_by_order(fun, order):
    """重复执行函数"""
    is_go_on = False
    for each in order:
        is_go_on = fun(each)
        if is_go_on is not True:
            break
    return is_go_on


# 重置文件

def initial_file(file_path_list):
    """
    指定path的文件，重置
    对于空文件，则创建
    :return:
    """
    for each in file_path_list:
        path = os.path.abspath(each)
        if not os.path.exists(path):
            f = open(path, 'a')
            f.close()
        else:
            f = open(path, 'w')
            f.close()
    return

# 追加写入

def write_2_file(file_path, ctx):
    """
    向指定目录写入文件
    :param path: 路径
    :param ctx: 内容
    :return:
    """
    path = os.path.abspath(file_path)
    with open(path, 'a', encoding='utf8') as f:
        f.write(ctx + '\n')
    return

def write_2_file_with_list(file_path, data_list):
    """
    向指定目录写入文件
    :param path: 路径
    :param ctx: 内容
    :return:
    """
    path = os.path.abspath(file_path)
    with open(path, 'a', encoding='utf8') as f:
        for each in data_list:
            f.write('\u0001'.join(each) + '\n')
    return

# 覆盖写入

def overwrite_file(file_path, ctx):
    """
    向指定目录写入文件
    :param path: 路径
    :param ctx: 内容
    :return:
    """
    path = os.path.abspath(file_path)
    with open(path, 'w', encoding='utf8') as f:
        f.write(ctx)
    return

# 保存图片

def save_img(file_path, img):
    """
    向指定目录保存下载图片
    :param file_path: 路径
    :param img: 内容
    :return:
    """
    path = os.path.abspath(file_path)
    with open(path, 'wb') as f:
        f.write(img)

# 解析json

def loads_json(json_text):
    """
    解析json
    :param json_text:
    :return:
    """
    js_dict = None
    try:
        js_dict = json.loads(json_text)
    except:
        logger.warning('json\tloads\t出错，请检查')
    return js_dict

# 写入json

def dumps_json(json_dict):
    return json.dumps(json_dict, ensure_ascii=False)

# 返回文本内容

def file_content(file_path):
    """返回文本内容
    如果是空文档呢
    """
    path = os.path.abspath(file_path)
    if not os.path.exists(path):
        f = open(path, 'w')
        f.close()
    return open(path, 'r', encoding='utf8').read()

# 解析lxml

def parse_lxml(html):
    """解析html"""
    selector = None
    try:
        selector = etree.HTML(html)
    except:
        logger.warning('lxml解析html时候出错')
    return selector

# 返回一个集合

def make_set(file_path, index, blank):
    """
    返回指定目录的集合
    :param file_path: 文件目录
    :param index: 索引位置
    :param blank: 分隔符
    :return:
    """
    path = os.path.abspath(file_path)
    if index != '' and blank != '':
        return set(i.strip().split(blank)[index] for i in open(path, 'r', encoding='utf8'))
    elif index == '' and blank != '':
        return set(i.strip().split(blank) for i in open(path, 'r', encoding='utf8'))
    else:
        return set(i.strip() for i in open(path, 'r', encoding='utf8'))

# 返回一个列表

def make_list(file_path, index, blank):
    """
    返回指定目录的集合
    :param file_path: 文件目录
    :param index: 索引位置
    :param blank: 分隔符
    :return:
    """
    path = os.path.abspath(file_path)
    if index != '' and blank !='':
        return [i.strip().split(blank)[index] for i in open(path, 'r', encoding='utf8')]
    elif index == '' and blank != '':
        return [i.strip().split(blank) for i in open(path, 'r', encoding='utf8')]
    else:
        return [i.strip() for i in open(path, 'r', encoding='utf8')]

# 返回一个生成器

def make_generator(file_path, blank):
    """
    返回一个生成器
    :param file_path:文件目录
    :param blank: 分隔符
    :return:
    """
    path = os.path.abspath(file_path)
    for i in open(path, 'r', encoding='utf8'):
        if blank != '':
            yield i.strip().split(blank)
        else:
            yield i.strip()

# translate

def translate_2_json_dict(ctx):
    """把redis返回的字符变成json能loads的字符串"""
    return ctx.decode().replace('\'', '"')


def redis_conn():
    """链接redis"""
    return StrictRedis(host=config.redis_host, port=config.redis_port, db=config.redis_db)
    # return StrictRedis(host=config.redis_host2, password=config.redis_password,port=config.redis_port, db=config.redis_db)


def push_2_que(que, ctx):
    """像指定的que push 数据"""
    try:
        redis_cli = redis_conn()
        if redis_cli is not None:
            redis_cli.lpush(que, ctx)
    except Exception as e:
        logger.warning('Redis推送数据出错,\t{0}'.format(e))


def wait_msg(que):
    """等待数据反馈"""
    msg = None
    try:
        redis_cli = redis_conn()
        if redis_cli.exists(que):
            msg = redis_cli.rpop(que)
    except Exception as e:
        logger.warning('Redis接受数据出错,\t{0}'.format(e))
    return msg


def clean_que(que_list):
    """将指定的que的数据清空，因为要保持队列的数据为最新的"""
    try:
        redis_cli = redis_conn()
        for que in que_list:
            while redis_cli.exists(que):
                redis_cli.rpop(que)

    except Exception as e:
        logger.warning('Redis清洗队列数据时出错,\t{0}'.format(e))

def recevice_msg_long(que):
    """等待指定队列有数据"""
    msg = None
    try:
        redis_cli = redis_conn()
        while True:
            if redis_cli.exists(que):
                # msg = redis_cli.rpop(que)
                msg = redis_cli.lpop(que)
                msg = loads_json(msg)
                break
            time.sleep(0.1)
    except Exception as e:
        logger.warning('Redis接受数据出错,\t{0}'.format(e))

    return msg

def static_msg_count(que):
    """统计指定的队列，有消息的数据"""
    count = 0
    msg_list = []
    try:
        redis_cli = redis_conn()
        while True:
            if redis_cli.exists(que):
                msg = redis_cli.rpop(que)
                if msg is not None:
                    msg_list.append(loads_json(msg))
                    count += 1
            else:
                break
        # 写入队列,这时候不用考虑先后问题
        if msg_list != []:
            for i in msg_list:
                redis_cli.lpush(que, dumps_json(i))

    except Exception as e:
        logger.warning('Redis统计\t{0}队列数量时候出错\t {1}'.format(que, e))
        print(e)
    return count
