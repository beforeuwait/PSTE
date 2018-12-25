# coding=utf-8


import time
import config as cnf
from copy import deepcopy
from HTTP import RequestAPI
from multiprocessing import Pool
from utils import loads_json


"""
    拿到参数 姓名+身份证
    调用被执行人接口和失信被执行人接口
    
"""

# type
_final_data = dict
_html = str
_zhixing_list = (list, int)
_query_data = list


# 与captcha模块通信
class CaptchaHandler():
    """
    反馈，索取新的验证码，都通过这个类去执行
    提供当前最新的验证码
    取新的验证码
    """
    def __init__(self):
        self.z_c_id = ''
        self.z_c_code = ''
        self.s_c_id = ''
        self.s_c_code = ''

    def receive_new_captcha(self, choice):
        """获取新的验证码"""
        if choice == 'zhixing':
            pass
        else:
            pass

    def get_new_captcha(self):
        """从消息队列获取最新的验证码"""
        pass

def executoer_for_web_server(name, card) -> _final_data:
    """接口调用, 传入参数"""
    # 拿到验证码
    # 请求接口
    # 先拿列表数据，再拿详情
    # 需要开2个进程同时去执行
    # pool = Pool(2)
    data = {}

    # data_z = get_zhixing_data(name, card)
    # print(data_z)
    data_s = get_shixin_data(name, card)
    # return data


def get_zhixing_data(name, card) -> _query_data:
    curr_page, pages = 1, 1
    retry = 3
    data_z = []
    http = RequestAPI()
    while curr_page <= pages and retry > 0:
        html = get_zhixing_list(name, card, curr_page,http)
        # 如果html = error 则说明该验证码无效
        if html == 'error':
            # 对于验证码错误，提交重试次数，重试为3
            # todo: 添加重新获取验证码部分
            retry -= 1
            continue
        data_list, pages = parse_zhixing_shixin_list(html)
        data_info = get_zhixing_each_info(data_list, http)
        data_z.extend(data_info)
        curr_page += 1
    return data_z


def get_zhixing_list(name, card, curr_page, http) -> _html:
    """获取被执行人数据"""
    url_z_list = cnf.url_z_list
    headers_z_list = cnf.headers_z_list
    payloads_z = deepcopy(cnf.payloads_z)
    # todo: 验证码装载部分
    payloads_z.update({
        'pName': name,
        'pCardNum': card,
        'captchaId': '204a24429b6643739835048a2e4e6fa4',
        'pCode': 'cyfe',
        'currentPage': curr_page
    })
    html = http.receive_and_request(url=url_z_list, headers=headers_z_list, payloads=payloads_z, method='post')
    return html


def parse_zhixing_shixin_list(data_list) -> _zhixing_list:
    """解析列表数据"""
    js_dict = loads_json(data_list)
    data, pages = [], 1
    if js_dict is not None:
        for each in js_dict[0].get('result'):
            name = each.get('pname') if each.get('pname') else each.get('iname')
            jsonObject = each.get('jsonObject')
            date = ''
            if jsonObject:
                d_dict = loads_json(jsonObject)
                date = d_dict.get('caseCreateTime') if d_dict.get('caseCreateTime') else d_dict.get('regDate')
            gisId = each.get('caseCode')
            pid = str(each.get('id'))
            data.append([name, date, gisId, pid])
        pages = js_dict[0].get('totalPage')
    return data, pages


def get_zhixing_each_info(data_list, http):
    """获取各执行人列表的详情"""
    data = []
    headers = cnf.headers_z_info
    url_info = cnf.url_z_info
    for each in data_list:
        pid = each[-1]
        params = deepcopy(cnf.params_z_info)
        params.update({
            'id': pid,
            'captchaId': '204a24429b6643739835048a2e4e6fa4',
            'j_captcha': 'cyfe',
            '_': int(time.time()*1000)
        })
        info = http.receive_and_request(url=url_info, headers=headers, params=params, method='get')
        if info == '{}':
            # 代表验证码错误
            pass
        data.append(loads_json(info))
    return data


def get_shixin_data(name, card):
    curr_page, pages = 1, 1
    retry = 3
    data_s = []
    http = RequestAPI()
    while curr_page <= pages and retry > 0:
        html = get_shixin_list(name, card, curr_page, http)
        if html == 'error':
            # 验证码重试
            retry -= 1
            continue
        data_list, pages = parse_zhixing_shixin_list(html)
        data_info = get_shixin_each_info(data_list, http)
        data_s.extend(data_info)
        curr_page += 1



def get_shixin_list(name, card, curr_page, http):
    """获取失信被执行人数据"""
    url_s_list = cnf.url_s_list
    headers = cnf.headers_s_list
    payloads_s = cnf.payloads_s
    payloads_s.update({
        'pName': name,
        'pCardNum': card,
        'captchaId': 'b708ae7d45a342379750a1d9c8e59b35',
        'pCode': 'se85',
        'currentPage': curr_page
    })
    html = http.receive_and_request(url=url_s_list, headers=headers, payloads=payloads_s, method='post')

    return html



def get_shixin_each_info(data_list, http):
    """获取各失信被执行人详情"""
    data = []
    headers = cnf.headers_s_info
    url = cnf.url_s_info
    for each in data_list:
        params = deepcopy(cnf.params_s_info)
        params.update({
            'id': each[-1],
            'caseCode': each[-2],
            'pCode': 'se85',
            'captchaId': 'b708ae7d45a342379750a1d9c8e59b35',
        })
        info = http.receive_and_request(url=url, headers=headers, params=params, method='get')
        if info == '{}':
            # 代表验证码错误
            # todo: 验证码更新
            pass
        else:
            data.append(loads_json(info))
    return data


if __name__ == '__main__':
    executoer_for_web_server(name='陈琪', card='33100319860901369X')