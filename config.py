# coding=utf8

import os
import logging

os.chdir(os.path.split(os.path.abspath(__file__))[0])

#   [other]

# 指定休息120秒
sleep_time = 20

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

captcha_count = 1

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

#   spider


params_dict = {
    'zhixing': {
        'searchCourtName': '全国法院（包含地方各级法院）',
        'selectCourtId': '1',
        'selectCourtArrange': '1',
        'pname': '王刚',
        'cardNum': '',
        'j_captcha': 'aFf2',
        'captchaId': '282a905ab0e64e90affaa997e763c7c1'
    },
    'shixin': {
        'pName': '王刚',
        'pCardNum': '',
        'pProvince': '0',
        'pCode': 'pxmq',
        'captchaId': '7c9240f22ee944fd96d184769c63be26'
    }
}

url_dict = {
    'zhixing': 'http://zhixing.court.gov.cn/search/newsearch',
    'shixin': 'http://zxgk.court.gov.cn/shixin/findDis'
}

headers_dict = {
    'zhixing': {
        'Host': 'zhixing.court.gov.cn',
        'Origin': 'http://zhixing.court.gov.cn',
        'Referer': 'http://zhixing.court.gov.cn/search/index_form.do'
    },
    'shixin': {
        'Host': 'zxgk.court.gov.cn',
        'Origin': 'http://zxgk.court.gov.cn',
        'Referer': 'http://zxgk.court.gov.cn/shixin/index_form.do'
    }
}

headers_info_dict = {
    'zhixing': {
        'Host': 'zhixing.court.gov.cn',
        'Referer': 'http://zhixing.court.gov.cn/search/',

    },
    'shixin': {
        'Host': 'zxgk.court.gov.cn',
        'Referer': 'http://zxgk.court.gov.cn/shixin/new_index.html',
    }
}

headers_main = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Content-Length': '271',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': '',
    'Origin': '',
    'Proxy-Connection': 'keep-alive',
    'Referer': '',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

headers_info = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Host': '',
    'Proxy-Connection': 'keep-alive',
    'Referer': '',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


url_info_dict = {
    'zhixing': 'http://zhixing.court.gov.cn/search/newdetail',
    'shixin': 'http://zxgk.court.gov.cn/shixin/disDetail'
}

params_info_dict = {
    'zhixing': {
        'id': '12780668',
        'j_captcha': 'ydwa',
        'captchaId': '282a905ab0e64e90affaa997e763c7c1',
        '_': '1538967156193',
    },
    'shixin': {
        'id': '704523825',
        'pCode': 'mgjx',
        'captchaId': '7c9240f22ee944fd96d184769c63be26'
    }
}

#   file

list_file = {
    'zhixing': './DB/zhixing_list.txt',
    'shixin': './DB/shixin_list.txt',
    'baidu': './DB/baidu_list.txt'
}

info_file = {
    'zhixing': './DB/zhixing_info.txt',
    'shixin': './DB/shixin_info.txt',
    'baidu': './DB/baidu_info.txt'
}

#   baidu

params_baidu = {
    'resource_id': '6899',
    'query': '失信被执行人名单',
    'cardNum': '',
    'iname': '王刚',
    'areaName': '',
    'pn': '10',
    'rn': '10',
    'ie': 'utf-8',
    'oe': 'utf-8',
    'format': 'json',
    't': '1538984600452',
    '_': '1538983980644',
}

headers_baidu = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'sp0.baidu.com',
    'Referer': 'https://www.baidu.com/s?wd=%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E4%BF%A1%E6%81%AF%E6%9F%A5%E8%AF%A2&rsv_spt=1&rsv_iqid=0xbbfc6e7d00002167&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=10&rsv_sug1=7&rsv_sug7=100&rsv_t=c0ffDlsDZ0XVT4QUp2qd%2BhFnnRcy5Re%2FgBUzdaQMEft%2FWIRKJ8pfi3rvlkJ7%2FaFw9QH9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

url_baidu = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'