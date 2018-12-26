# coding=utf-8

"""
    该api的配置文件

    从三个数据源减少到2个：
        1. 被执行人
        2. 失信被执行人
        3. 百度api （取消）

    # 影响性能的因素：

    1. 验证码的准确率
    2. 服务器的性能，遇到压力大时候会抽风
"""

# 验证码

url_ocr = 'http://47.97.181.94:21000/pstecaptcha'

url_z = 'http://zhixing.court.gov.cn/search/'

url_s = 'http://zxgk.court.gov.cn/shixin/'

headers_z = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Host': 'zhixing.court.gov.cn',
    # 'Cookie': '_gscu_1138507821	41398408liscqj19',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

headers_s = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Host': 'zxgk.court.gov.cn',
    # 'Cookie': '_gscu_1138507821	41398408liscqj19',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://zxgk.court.gov.cn/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

url_z_c = 'http://zhixing.court.gov.cn/search/captcha.do?captchaId={0}&random={1}'

url_s_c = 'http://zxgk.court.gov.cn/shixin/captchaNew.do?captchaId={0}&random={1}'

# 验证验证码

url_z_y = 'http://zhixing.court.gov.cn/search/checkyzm?captchaId={0}&pCode={1}'

url_s_y = 'http://zxgk.court.gov.cn/shixin/checkyzm.do?captchaId={0}&pCode={1}'

headers_s_y = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Host': 'zxgk.court.gov.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://zxgk.court.gov.cn/shixin/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

headers_z_y = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Host': 'zhixing.court.gov.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://zhixing.court.gov.cn/search/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# 被执行人

url_z_list = 'http://zhixing.court.gov.cn/search/searchBzxr.do'

url_z_info = 'http://zhixing.court.gov.cn/search/newdetail'

headers_z_list = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Length': '282',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'zhixing.court.gov.cn',
    'Origin': 'http://zhixing.court.gov.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://zhixing.court.gov.cn/search/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

headers_z_info = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Host': 'zhixing.court.gov.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://zhixing.court.gov.cn/search/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

payloads_z = {
    'pName': '张亮',
    'pCardNum': '',
    'selectCourtId': '0',
    'pCode': '',
    'captchaId': '',
    'searchCourtName': '全国法院（包含地方各级法院）',
    'selectCourtArrange': '1',
    'currentPage': '1'
}

params_z_info = {
    'id': '25856865',
    'j_captcha': '',
    'captchaId': '',
    '_': '1545617060876'
}

# 失信被执行人
url_s_list = 'http://zxgk.court.gov.cn/shixin/searchSX.do'

url_s_info = 'http://zxgk.court.gov.cn/shixin/disDetailNew'

headers_s_list = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Length': '114',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'zxgk.court.gov.cn',
    'Origin': 'http://zxgk.court.gov.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://zxgk.court.gov.cn/shixin/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

headers_s_info = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Host': 'zxgk.court.gov.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://zxgk.court.gov.cn/shixin/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

payloads_s = {
    'pName': '张亮',
    'pCardNum': '',
    'pProvince': '0',
    'pCode': '',
    'captchaId': '',
    'currentPage': '1'
}

params_s_info = {
    'id': '',
    'caseCode': '',
    'pCode': '',
    'captchaId': '',
}


# redis

redis_cnf = {
    'host': 'localhost',
    'port': 6379,
    'db': 5,
    'que_z': 'captcha_z',
    'que_s': 'captcha_s',
}
