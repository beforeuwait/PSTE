# coding=utf8

"""
- author = wangjiawei
- date = 2018-10-08

- quote: pste 的web服务

"""


from copy import deepcopy
import tornado.web
from tornado.ioloop import IOLoop
from multiprocessing import Pool
from PsteSpider import run
from utils import dumps_json


class MainHandler(tornado.web.RequestHandler):

    param_names = ['pname', 'cardNum']

    api_demo = {
        "api_status_code": 200,
        "api_msg": [],
        "api_status": "success",
        "data": {
            'zhixing': {
                'info': [],
                'status': 200
            },
            'shixin': {
                'info': [],
                'status': 200
            },
            'baidu': {
                'info': [],
                'status': 200
            }
        }
    }

    def get(self):
        self.write('welcome')

    def post(self):
        api_info = self.lets_do_spider()
        self.write(api_info)
        del api_info


    def lets_do_spider(self):
        """针对2.0版本"""
        result = []
        api_info = deepcopy(self.api_demo)
        # 省略了参数验证环节
        pname = self.get_argument('pname')
        cardNum = self.get_argument('cardNum')
        # 使用多进程
        pool = Pool(3)
        duty_list = ['zhixing', 'shixin', 'baidu']
        for duty in duty_list:
            result.append(pool.apply_async(run, (duty, pname, cardNum,)))

        pool.close()
        pool.join()
        # 更新被执行人
        api_info['data']['zhixing'] = result[0].get()
        # 更新失信被执行人
        api_info['data']['shixin'] = result[1].get()
        # 更新百度
        api_info['data']['baidu'] = result[2].get()

        return dumps_json(api_info)




application = tornado.web.Application([(r"/pste2", MainHandler),])


if __name__ == "__main__":
    application.listen(23080)
    IOLoop.instance().start()
