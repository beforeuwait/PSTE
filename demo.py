# coding=utf8

"""


"""

import time
import requests
from HTTP.RequestServerApi import RequestAPI

params = {
    'searchCourtName': '全国法院（包含地方各级法院）',
    'selectCourtId': '1',
    'selectCourtArrange': '1',
    'pname': '王刚',
    'cardNum': '511324199012120034',
    'j_captcha': 'aFf2',
    'captchaId': '282a905ab0e64e90affaa997e763c7c1',
}

url = 'http://zhixing.court.gov.cn/search/newsearch'

urls = 'http://zhixing.court.gov.cn/search/newdetail?id=12780668&j_captcha=2ura&captchaId=282a905ab0e64e90affaa997e763c7c1&_=1538967156193'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Content-Length': '271',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'zhixing.court.gov.cn',
    'Origin': 'http://zhixing.court.gov.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://zhixing.court.gov.cn/search/index_form.do',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
proxy = {
        "http": "http://HUICU80ZV6SK58WP:21CE6FB2A2AE49B0@http-pro.abuyun.com:9010",
        "https": "http://HUICU80ZV6SK58WP:21CE6FB2A2AE49B0@http-pro.abuyun.com:9010",
    }

# api = RequestAPI()
# res = requests.get(urls, headers=headers, data=params, proxies=proxy)
# res = api.receive_and_request(url=urls, headers=headers, method='GET')
# print(res.status_code)
# print(res.content.decode('utf8'))

url1 = 'http://localhost:23000/pste'

data = {'pname': '姚春', 'cardNum': '379009197010016016'}
s = time.time()
res = requests.post(url1, data=data)
d = time.time()

print(res.status_code)
print(res.content.decode('utf8'))
print('耗时', d-s)