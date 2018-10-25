# coding=utf8


"""
- authot = wangjiawei
- date = 2018-10-08
- info = 失信被执行人抓取脚本

quote:

todo list:
    1. 被执行人抓取
    2. 失信被执行人抓取
    3. 百度上被执行人数据抓取

    接口输入的参数
    params = {
        'searchCourtName': '全国法院（包含地方各级法院）',
        'selectCourtId': '1',
        'selectCourtArrange': '1',
        'pname': '王刚',
        'cardNum': '',
        'j_captcha': 'aFf2',
        'captchaId': '282a905ab0e64e90affaa997e763c7c1',
        }
    流程同实行被执行人通用:
    1. 接受参数，获取被执行人参数 pname, cardNum
    2. 从队列获取验证码信息
    3. 反馈，错误的反馈，正确的反馈，都要告诉验证码
    4. 返回数据

    数据说明:
    拿到数据详情，返回详情。

    ** 会出现302的情况，代表服务器查询过多，压力大
"""

import time
import re
import os
import config
import logging
from copy import deepcopy
from HTTP.RequestServerApi import RequestAPI
import HTTP.requests_server_config as scf
from utils import parse_lxml
from utils import loads_json
from utils import push_2_que
from utils import recevice_msg_long
from utils import dumps_json
from utils import write_2_file_with_list
from utils import write_2_file

spider_log = logging.getLogger()

spider_log.setLevel(logging.INFO)   # 定义为INFO是因为requests要写debug
request_handler = logging.FileHandler(os.path.abspath('./log/spider.log'))
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
request_handler.setFormatter(fmt)
spider_log.addHandler(request_handler)


class NewRequestAPI(RequestAPI):
    """需要重写状态码部分"""

    def do_request(self, url, method, params, payloads, allow_redirects):
        """根据指定的请求方式去请求"""
        retry = scf.retry
        html = 'null_html'
        # 有的网页直接反空，不建议用空，不好去分析原因,
        while retry > 0:
            response = None
            try:
                # 选择执行的方式
                if method == 'GET':
                    # 请求前判断是否有参数，有的话添加到session里,请求后则删除
                    self.update_params(params)
                    response = self.GET_request(url, allow_redirects)
                    self.discard_params()

                elif method == 'POST':
                    response = self.POST_request(url, payloads)

            except Exception as e:
                # 输出log, 这里的错误都是网络上的错误
                scf.http_logger.info('请求出错, 错误原因:\t{0}'.format(e), extra=scf.filter_dict)
                time.sleep(scf.error_sleep)

            else:
                # 拿到response后，处理
                status_code = response.status_code

                if status_code == 302:
                    html = 'wrong_request'
                    break
                elif status_code < 300:
                    try:
                        html = response.content.decode(scf.ec_u)
                    except:
                        html = response.text
                    break
            retry -= 1
        return html


class GenerallySpider():
    """针对被执行人、失信被执行人的通用请求脚本"""

    pname = ''
    cardNum = ''
    name = 'general'
    params = config.params_dict
    j_captcha = ''
    captchaId = ''
    pCode = ''
    fb = 'feedback'

    def feedback(self):
        """在调用这个函数，就是告知验证码识别模块，当前的验证码无效"""
        que = config.que.get('feedback')
        # 发送任意消息
        push_2_que(que, '1')

    def pop_captcha_info(self):
        """
        从指定的队列拿到指定的验证码数据
        """
        pass

    def construct_params(self):
        """构建执行的params"""
        # 这个由各spider自定义去弄
        pass

    def construct_params_info(self, oid):
        """构建详情的params
        oid 代表改案件的id
        """
        # 这个也是由各spider自定义去弄
        pass


    def main_logic(self):
        """主逻辑，组装好params，
        请求数据，解析结果
        拿完全部，以及每一条详情

        """
        info = []

        # 验证码失效的时候回收的信息
        recycle = []

        list_file = config.list_file.get(self.name)

        # 被执行人和实行被执行人的网址不同
        url = config.url_dict.get(self.name)
        # 构建请求头然后请求获取数据
        headers = config.headers_main
        headers.update(config.headers_dict.get(self.name))

        headers_info = config.headers_info
        headers_info.update(config.headers_info_dict.get(self.name))

        api = NewRequestAPI()
        current_page, pages = 1, 1

        not_break, retry = True, 1
        while current_page <= pages and not_break:
            # 允许带着错误验证码的重试的次数为3
            if retry > 2:
                not_break = False
            self.params.update({'currentPage': current_page})
            html = api.receive_and_request(url=url, headers=headers, payloads=self.params, method='POST')
            if html != 'null_html':
                data, pages = self.parse_list_and_pages(html)
                # 对data进行判断
                if data is None:
                    # 重新获取验证码返回从新执行
                    self.feedback()
                    self.pop_captcha_info()
                    retry += 1
                    continue
                # 获取每个的详情
                else:
                    # 记录数据
                    write_2_file_with_list(list_file, data)
                    info, recycle = self.lets_fuck_recycle(data)
            elif html == 'wrong_request':
                # 针对查询过多出现的302的处理
                info = ['当前查询过多，稍后再试']
                break

            current_page += 1
        del api
        # 抓取完毕返回数据
        # 对recycle进行再次抓取
        while recycle != []:
            recycle_list, recycle = self.lets_fuck_recycle(recycle)
            info.extend(recycle_list)

        return info

    def lets_fuck_recycle(self, data):
        """这个函数的作用就是炒回锅肉"""
        info = []
        recycle = []

        info_file = config.info_file.get(self.name)

        url_info = config.url_info_dict.get(self.name)

        headers_info = config.headers_info
        headers_info.update(config.headers_info_dict.get(self.name))

        api = RequestAPI()

        for each in data:
            params_info = self.construct_params_info(each[-1])
            json_text = api.receive_and_request(url=url_info, headers=headers_info, params=params_info, method='GET')
            # 需要验证是否有数据
            js_dict = self.verify_json_text(json_text)
            if js_dict is not None:
                # 放回数据
                info.append(js_dict)
                # 记录数据
                write_2_file(info_file, dumps_json(js_dict))
            else:
                self.feedback()
                self.pop_captcha_info()
                recycle.append(each)

            del params_info
        return info, recycle

    def verify_json_text(self, json_text):
        """验证返回的数据是否为正常"""
        js_dict = loads_json(json_text)
        return js_dict


    def parse_list_and_pages(self, html):
        selector = parse_lxml(html)
        data = []
        pages = 1
        if selector is not None:
            data_list = selector.xpath('//table[@class="Resultlist"]/tbody/tr')
            # 如果为空，则验证码失效
            if data_list == []:
                # 通过对data 为None还是为[]来判断是否有验证码通过
                data = None

                return data, pages
            # 获取总页数
            pages = int(re.findall('var totalPage = (\d{1,3})', html, re.S)[0]) if\
                re.findall('var totalPage = (\d{1,3})', html, re.S) else 1
            for each in data_list:
                if each.xpath('th'):
                    continue
                name = each.xpath('td[2]/text()')[0] if each.xpath('td[2]/text()') else None
                date = each.xpath('td[3]/text()')[0] if each.xpath('td[3]/text()') else None
                gisId = each.xpath('td[4]/text()')[0] if each.xpath('td[4]/text()') else None
                pid = each.xpath('td[5]/a/@id')[0] if each.xpath('td[5]/a/@id') else None
                if name is not None and date is not None and gisId is not None and pid is not None:
                    data.append([name, date, gisId, pid])
        return data, pages

class ZhixingSpider(GenerallySpider):
    """
    负责获取被执行人的数据抓取

    """
    name = 'zhixing'

    def __init__(self, pname, cardNum):
        self.pname = pname
        self.cardNum = cardNum

    def construct_params(self):
        # 先获取captcha
        self.pop_captcha_info()
        # 再更新params
        self.params = config.params_dict.get(self.name)
        self.params.update({'pname': self.pname,
                            'cardNum': self.cardNum,
                            'captchaId': self.captchaId,
                            'j_captcha': self.j_captcha})


    def pop_captcha_info(self):
        """
        从指定的队列拿到指定的验证码数据
        """
        que = config.que.get(self.name)
        captcha = recevice_msg_long(que)
        self.captchaId = captcha[0][0]
        self.j_captcha = captcha[0][1].lower()


    def construct_params_info(self, oid):
        """构建详情需要的params"""
        params_info = deepcopy(config.params_info_dict.get(self.name))
        params_info.update({'id': oid,
                            'captchaId': self.captchaId,
                            'j_captcha': self.j_captcha,
                            '_': round(time.time()*1000)
                            })
        return params_info

    def do(self):
        self.construct_params()
        info = self.main_logic()
        return info


class ShixinSpider(GenerallySpider):
    """
    负责失信被执行人的数据抓取
    """
    name = 'shixin'

    def __init__(self, pname, cardNum):
        self.pname = pname
        self.cardNum = cardNum

    def pop_captcha_info(self):
        """
        从指定的队列拿到指定的验证码数据
        """
        que = config.que.get(self.name)
        captcha = recevice_msg_long(que)
        self.captchaId = captcha[0][0]
        self.pCode = captcha[0][1].lower()


    def construct_params(self):
        # 先获取captcha
        self.pop_captcha_info()
        # 再更新params
        self.params = config.params_dict.get(self.name)
        self.params.update({'pName': self.pname,
                            'pCardNum': self.cardNum,
                            'captchaId': self.captchaId,
                            'pCode': self.pCode})

    def construct_params_info(self, oid):
        """构建详情需要的params"""
        params_info = deepcopy(config.params_info_dict.get(self.name))
        params_info.update({'id': oid,
                            'captchaId': self.captchaId,
                            'pCode': self.pCode
                            })
        return params_info

    def do(self):
        self.construct_params()
        info = self.main_logic()
        return info

class BaiduSpider():
    """
    负责从百度的api获取数据
    """
    name = 'baidu'
    params = config.params_baidu
    url = config.url_baidu
    headers = config.headers_baidu
    baidu_list = config.list_file.get(name)

    def __init__(self, pname, cardNum):
        self.pname = pname
        self.cardNum = cardNum

    def construct_params(self):
        self.params.update({'iname': self.pname,
                            'cardNum': self.cardNum,
                            't': round(time.time()*1000),
                            '_': round(time.time()*1000)})


    def main_logic(self):
        """百度失信被执行人数据采集
        有翻页的可能哦
        """
        info = []
        self.construct_params()
        api = RequestAPI()
        num, total_num = 1, 50
        while num*50 <= total_num:
            self.params.update({'pn': num*10})
            html = api.receive_and_request(url=self.url, headers=self.headers, params=self.params, method='GET')
            if html != 'null_html':
                info_temp, total_num = self.parase_html(html)
                if info_temp != []:
                    info.extend(info_temp)
            num += 1
        # 完成抓取后，返回结果
        return info

    def parase_html(self, html):
        info = []
        total_num = 1
        js_dict = loads_json(html)
        if js_dict is not None:
            data = js_dict.get('data')
            if isinstance(data, list) and data != []:
                for i in data:
                    for each in i.get('result'):
                        info.append(each)
                        # 放入持久化
                        write_2_file(self.baidu_list, dumps_json(each))
                    # 还需要判断是否有下一页
                    total_num = i.get('dispNum', 1)
        return info, total_num

    def do(self):
        info = self.main_logic()
        return info

# 启动函数
def run(choice, pname, cardNum):
    """这个run函数
    承担三个作用:
    1.被执行人数据抓取
    2.失信被执行人数据抓取
    3.百度失信被执行人数据抓取

    根据相应的处理，发布不同的任务
    """
    spider_log.debug('接收任务\t{0}'.format(choice))
    switch = {
        'zhixing': ZhixingSpider,
        'shixin': ShixinSpider,
        'baidu': BaiduSpider
    }
    # 实例化选择
    m = switch.get(choice)(pname, cardNum)
    info = m.do()
    del m
    return info
