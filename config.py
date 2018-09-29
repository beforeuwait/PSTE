# coding=utf8

import os
import logging

os.chdir(os.path.split(os.path.abspath(__file__))[0])

#   [other]

# 指定休息120秒
sleep_time = 120

#   [logger]

logger = logging.getLogger('main')

logger.setLevel(logging.DEBUG)   # 定义为INFO是因为requests要写debug
request_handler = logging.FileHandler(os.path.abspath('./log/run.log'))
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
request_handler.setFormatter(fmt)
logger.addHandler(request_handler)

#   【proxy】

proxy = {
        "http": "http://HUICU80ZV6SK58WP:21CE6FB2A2AE49B0@http-pro.abuyun.com:9010",
        "https": "http://HUICU80ZV6SK58WP:21CE6FB2A2AE49B0@http-pro.abuyun.com:9010",
    }

#   【CaptchaHandler】

captcha_count = 2

host_zs = {
    'zhixing': 'zhixing.court.gov.cn',
    'shixin': 'zxgk.court.gov.cn'
}

headers_CaptchaHandler = {
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Host': '',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://zhixing.court.gov.cn/search/index_form.do',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

headers_host = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Host': '',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'https://www.baidu.com/link?url=KF8Khh9dCKlXaSVfgBqRtd_efJm8_TIf3EqkSgxkkMTOuuqQCL-ttrHPyzRaIeUo&wd=&eqid=f4cc9418000cb44d000000055bad95b3',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

url_captcha_zhixing = 'http://zhixing.court.gov.cn/search/captcha.do'

url_captcha_shixin = 'http://zxgk.court.gov.cn/shixin/captcha.do'

url_host = 'http://zhixing.court.gov.cn/search/'

url_iframe_zhixing = 'http://zhixing.court.gov.cn/search/index_form.do'

url_iframe_shixin = 'http://zxgk.court.gov.cn/shixin/index_form.do'

url_svm = 'http://47.97.181.94:21000/pstecaptcha'

params_captcha = {
    'captchaId': 'cc848f9030274b5a91601800045d3346',
    'random': '0.988618299575891',
}

img_file = './img/{}.jpg'

file_captcha_zhixing = './DB/captcha_id_zhixing.txt'
file_captcha_shixin = './DB/captcha_id_shixin.txt'

file_captcha_zhixing_h = './DB/captcha_id_zhixing_history.txt'
file_captcha_shixin_h = './DB/captcha_id_shixin_history.txt'


#   [redis]

# 管道

que = {
    'zhixing': 'zx',
    'shixin': 'sx',
    'feedback': 'fb'
}

redis_host = 'localhost'
redis_port = 6379
redis_db = 11

