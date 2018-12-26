# coding=utf-8

"""
    验证码处理模块
    既然页面加入了验证码的前端验证
    在识别结束后，对验证码做一个验证，正确的放入队列里

"""

import time
import logging
import random
import base64
import config as cnf
from copy import deepcopy
from HTTP import RequestAPI
from HTTP.utils import MethodCheckError
from utils import load_selector
from utils import loads_json
from utils import connect_2_redis
from utils import json_dumps


# type
_captcha_html = tuple
_captcha_list = list
_ocr_result = list

# log
logger = logging.getLogger('captcha')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('./captcha_log.log')
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(fmt)
logger.addHandler(handler)

class Http(RequestAPI):

    def user_define_request(self, **kwargs):
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
        html = resp[0]
        [self.dr.sh.discard_cookie_headers_params(i) for i in ['headers', 'cookies', 'params']]
        self.dr.sh.close_session()

        return html


def request_home_page_2_get_captcha_id(http) -> _captcha_html:
    """请求2个部分的主页，获取captchaId"""
    html_z = http.receive_and_request(url=cnf.url_z, headers=cnf.headers_z, method='get')
    html_s = http.receive_and_request(url=cnf.url_s, headers=cnf.headers_s, method='get')
    return (html_z, html_s)


def parse_captcha_id(html_tuple) -> _captcha_list:
    cap_id = []
    for each in html_tuple:
        selector = load_selector(each)
        if selector is not None:
            captcha_id = selector.xpath('//input[@id="captchaId"]/@value')[0] \
                if selector.xpath('//input[@id="captchaId"]/@value') else None
            cap_id.append(captcha_id)
    return cap_id


def download_pic_and_ocr(captcha_list, http) -> _ocr_result:
    url_ocr = cnf.url_ocr
    url_z = deepcopy(cnf.url_z_c).format(captcha_list[0], random.random())
    url_s = deepcopy(cnf.url_s_c).format(captcha_list[1], random.random())
    img_z = http.user_define_request(url=url_z, headers=cnf.headers_z, method='get')
    img_s = http.user_define_request(url=url_s, headers=cnf.headers_s, method='get')
    payloads_z = {
        'pic': base64.b64encode(img_z),
        'type': 'pste'
    }
    payloads_s = {
        'pic': base64.b64encode(img_s),
        'type': 'pste'
    }
    result_z = http.receive_and_request(url=url_ocr, payloads=payloads_z, method='post')
    result_s = http.receive_and_request(url=url_ocr, payloads=payloads_s, method='post')

    result_dict_z = loads_json(result_z)
    result_dict_s = loads_json(result_s)
    captcha_z, captcha_s = None, None
    if result_dict_s and result_dict_z:
        if result_dict_s.get('status_code') == 200:
            captcha_s = result_dict_s.get('data').get('captcha')

        if result_dict_z.get('status_code') == 200:
            captcha_z = result_dict_z.get('data').get('captcha')

    return [[captcha_list[0], captcha_z], [captcha_list[1], captcha_s]]

# 验证码验证环节，通过验证，则放入队列，没通过则重试

def verify_ocr_push_que(captcha_tuple, http, cli) -> bool:
    """验证以及放入队列"""
    result = True
    captcha_z = captcha_tuple[0]
    captcha_s = captcha_tuple[1]
    url_z = deepcopy(cnf.url_z_y).format(captcha_z[0], captcha_z[1])
    url_s = deepcopy(cnf.url_s_y).format(captcha_s[0], captcha_s[1])
    headers_z = cnf.headers_z_y
    headers_s = cnf.headers_s_y
    resp_z = http.receive_and_request(url=url_z, headers=headers_z, method='get')
    resp_s = http.receive_and_request(url=url_s, headers=headers_s, method='get')
    logger.debug('z_status:\t{0}\ts_status:\t{1}'.format(resp_z.strip(), resp_s.strip()))
    if resp_z == '0':
        # 通过验证:
        result = False
    else:
        # 推入队列
        cli.lpush('captcha_z', json_dumps(captcha_z))
    if resp_s == '0':
        # 通过验证
        result = False
    else:
        # 推入队列
        cli.lpush('captcha_s', json_dumps(captcha_s))
    return result


# 主逻辑部分

def main_logic():
    """做4件事
    1. 拿到最新的captchaId
    2. 拿到id对应的img
    3. ocr以及验证
    4. 放入队列
    """
    cli = connect_2_redis()
    while True:
        http = Http()
        htmls = request_home_page_2_get_captcha_id(http)
        captcha_ids = parse_captcha_id(htmls)
        captcha_tuple = download_pic_and_ocr(captcha_ids, http)
        logger.debug(captcha_tuple)
        result = verify_ocr_push_que(captcha_tuple, http, cli)
        if not result:
            time.sleep(0.5)
            continue
        else:
            # 队列里只有21条可用数据
            cli.ltrim('captcha_z', 0, 20)
            cli.ltrim('captcha_s', 0, 20)
            time.sleep(1.5)


if __name__ == '__main__':
    main_logic()
