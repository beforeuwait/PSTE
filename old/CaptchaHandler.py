# coding=utf8

"""
info:

- author:   wangjiawei
- date  :   2018-09-28
-quote  :   失信被执行人验证码处理，该脚本负责去请求验证码，然后做识别

update:

    2018-09-29:
        完成验证码部分的识别，将不做图片保存处理，直接在线ocr
    2018-10-08:
        更新逻辑
        1. 请求captchaID时候偶尔会出现拿不到数据的情况,遇到这类情况，立马重新执行
        2. 配合spider，队里只放一个最新的captcha
        3. 针对ocr不是200的情况，都立马重新执行

    2018-10-29:
        更新验证码逻辑
        1. 验证码在队列的数量更改为10个
        2. 方式为FIFO (由spider在调取时候)
        3. 始终维持队列里的验证码数据为10个

    2018-10-30:
        修改bug，修改计时错误的问题
"""

import os
import random
import time
import base64
import logging
from HTTP.RequestServerApi import RequestAPI
import HTTP.requests_server_config as scf
from utils import parse_lxml
from utils import loads_json
from utils import dumps_json
from utils import initial_file
from utils import push_2_que
from utils import do_fun_cycle
from utils import do_fun_cycle_by_order
from utils import overwrite_file
from utils import clean_que
from utils import static_msg_count
import config


logger = logging.getLogger()

logger.setLevel(logging.INFO)   # 定义为INFO是因为requests要写debug
request_handler = logging.FileHandler(os.path.abspath('./log/captcha.log'))
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
request_handler.setFormatter(fmt)
logger.addHandler(request_handler)
"""负责请求iframe，然后拿到captcha_id,保存下来"""


def get_captcha_id():
    """去下载一个captchaId
    进入主页，找到标签，拿到结果
    这里有两个id，一个是 被执行人 一个是失信被执行人
    """
    file_shixin = config.file_captcha_shixin
    file_zhixin = config.file_captcha_zhixing

    file_shixin_h = config.file_captcha_zhixing_h
    file_zhixin_h = config.file_captcha_shixin_h

    headers = config.headers_host
    headers.update({'Host': config.host_zs.get('zhixing')})
    headers_zhixing = headers
    headers.update({'Host': config.host_zs.get('shixin')})
    headers_shixin = headers
    url_zhixing = config.url_iframe_zhixing
    url_shixin = config.url_iframe_shixin

    # 实例化请求模块
    ra = RequestAPI()
    html_zhixing = ra.receive_and_request(url=url_zhixing, headers=headers_zhixing, method='GET')
    html_shixin = ra.receive_and_request(url=url_shixin, headers=headers_shixin, method='GET')

    if html_zhixing != 'null_html' and html_shixin != 'null_html':
        captcha_id_zhixing = parse_captcha_id(html_zhixing)
        captcha_id_shixin = parse_captcha_id(html_shixin)

        if captcha_id_shixin is not None and captcha_id_zhixing is not None:
            # 做存储

            # 放入各自的文件里

            overwrite_file(file_path=file_shixin_h, ctx=captcha_id_shixin)
            overwrite_file(file_path=file_zhixin_h, ctx=captcha_id_zhixing)
            overwrite_file(file_path=file_zhixin, ctx=captcha_id_zhixing)
            overwrite_file(file_path=file_shixin, ctx=captcha_id_shixin)

            logger.info('完成captcha id 获取并写入')
        else:
            logger.warning('未完成captcha id 获取')
    else:
        logger.warning('获取captcha id 请求html过程失败')

def parse_captcha_id(html):
    selector = parse_lxml(html)
    captcha_id = None
    if selector is not None:
        captcha_id = selector.xpath('//input[@id="captchaId"]/@value')[0] \
            if selector.xpath('//input[@id="captchaId"]/@value') else None

    return captcha_id


"""负责请求captcha_id对于的图片，然后完成ocr，放入文件？队列?"""


def download_img_and_ocr(type):
    """同样的去请求，然后拿到数据
    需要去重写 requestAPI的 do_request
    下载的过程，将 zhixing 和 shixin文件里的captchaId都下载
    给个开关

    # 2018-10-29 在每次执行最后，将文件清空
    """
    is_go_on = False

    headers = config.headers_CaptchaHandler
    captcha_list = []
    if type == 'zhixing':
        captcha = config.file_captcha_zhixing
        headers.update({'Host': config.host_zs.get('zhixing')})

    else:
        captcha = config.file_captcha_shixin
        headers.update({'Host': config.host_zs.get('shixin')})
    for i in open(captcha, 'r', encoding='utf8'):
        url = config.url_captcha_zhixing if type == 'zhixing' else config.url_captcha_shixin
        params = config.params_captcha
        params.update({'captchaId': i.strip(), 'random': random.random()})
        # 开始请求

        logger.info('下载验证码图片\t{0}\t{1}'.format(type, i.strip()))
        di = Download_img()
        img = di.receive_and_request(url=url, headers=headers, params=params, method='GET')
        if img != 'null_html':
            """
            # 保存图片
            file_path = config.img_file.format(captcha)
            save_img(file_path=file_path, img=img)
            """
            # 执行ocr
            url = config.url_svm
            img_d = base64.b64encode(img)
            payloads = {
                'pic': img_d,
                'type': 'pste'
            }
            result = di.receive_and_request(url=url, payloads=payloads, method='POST')
            try:
                result_dict = loads_json(result)
                if result_dict.get('status_code') == 200:

                    captcha_list.append([i.strip(), result_dict.get('data').get('captcha')])
                    logger.info('完成图片ocr\t{0}\t{1}'.format(type, i.strip()))
                    is_go_on = True


            except Exception as e:
                logger.warning('ocr识别失败\t{0}'.format(e))

        else:
            logger.warning('下载验证码图片失败\t{0}\t{1}'.format(type, i.strip()))

    # 丢入队列里
    # 先要加入一个判断，列表不为空则行

    if captcha_list != []:
        que = config.que.get(type)
        logger.debug(captcha_list)
        push_2_que(que, dumps_json(captcha_list))
        logger.debug('ocr结果推入队列')

    return is_go_on


class Download_img(RequestAPI):

    def __init__(self):
        super(Download_img, self).__init__()

    def do_request(self, url, method, params, payloads, allow_redirects):
        """根据指定的请求方式去请求"""
        retry = scf.retry
        # 有的网页直接反空，不建议用空，不好去分析原因,
        html = 'null_html'
        while retry > 0:
            response = None
            try:
                if method == 'GET':
                    self.update_params(params)
                    response = self.GET_request(url, allow_redirects)
                    self.discard_params()
                elif method == 'POST':
                    response = self.POST_request(url=url, payloads=payloads)
            except Exception as e:
                # 输出log, 这里的错误都是网络上的错误
                scf.http_logger.info('请求出错, 错误原因:\t{0}'.format(e), extra=scf.filter_dict)
                time.sleep(scf.error_sleep)
            else:
                # 拿到response后，处理
                html = response.content
                break
            retry -= 1
            time.sleep(scf.r_sleep)
        return html

"""主逻辑模块"""

def main_theme():
    """主逻辑模块
    1. 获取id
    2. ocr
    3. 放队列
    4. 监听feedback
    5.循环
    """
    file_shixin = config.file_captcha_shixin
    file_zhixin = config.file_captcha_zhixing
    que_list = [config.que.get('zhixing'), config.que.get('shixin'), config.que.get('feedback')]

    """
    while True:
        # 获取id, 执行和失信同时获取各一个
        # 清空队列
        clean_que(que_list)
        # 清空文件
        initial_file([file_shixin, file_zhixin])
        # 按指定次数去迭代
        do_fun_cycle(get_captcha_id, captcha_count)
        # 执行ocr
        is_go_on = do_fun_cycle_by_order(download_img_and_ocr, ['zhixing', 'shixin'])
        if not is_go_on:
            # 失败ocr,重试
            logger.warning('ocr发生错误，重试')
            time.sleep(0.1)
            continue
        # 接下来休眠时间同时监听
        start = time.time()
        while int(time.time() - start) < sleep_time:
            # 监听数据
            msg = wait_msg(fb_que)
            if msg:
                break
    """
    # 2018-10-29: 执行新逻辑
    # 在有效期2分钟内，要始终保持队列20个可用的，任意监听一个队列就行
    clean_que(que_list)

    start = time.time()

    while True:

        # 统计消息队列个数
        count = static_msg_count(que_list[0])
        # 开始运行
        # 按指定次数去迭代
        if count < 10:
            """
            # 该方法是作为先下载齐需要的，这个行不通
            do_fun_cycle(get_captcha_id, 20-count)
            # 执行ocr
            do_fun_cycle_by_order(download_img_and_ocr, ['zhixing', 'shixin'])
            """
            for i in range(10-count):
                do_fun_cycle(get_captcha_id, 1)
                # 执行ocr
                do_fun_cycle_by_order(download_img_and_ocr, ['zhixing', 'shixin'])


        if time.time() - start > 120:
            # 超过2分钟，全部验证码失效，重新开始获取验证码
            # 清空队列
            clean_que(que_list)
            # 清空文件
            initial_file([file_shixin, file_zhixin])
            start = time.time()

        else:
            time.sleep(0.1)


if __name__ == '__main__':
    main_theme()
