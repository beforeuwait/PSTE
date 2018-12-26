# coding=utf8

"""
- author = wangjiawei
- date = 2018-10-08

- quote: pste 的web服务

"""


import tornado.web
from tornado.ioloop import IOLoop
from utils import json_dumps
from pste_spider import executoer_for_web_server
from utils import logger

class MainHandler(tornado.web.RequestHandler):

    param_names = ['pname', 'cardNum']

    def get(self):
        self.write('welcome')

    def post(self):
        api_info = self.lets_do_spider()
        self.write(api_info)
        del api_info


    def lets_do_spider(self):
        """针对2.0版本"""
        # 省略了参数验证环节
        pname = self.get_argument('pname')
        cardNum = self.get_argument('cardNum')
        # 使用多进程
        logger.debug('接受参数:\t{0}\t{1}'.format(pname, cardNum))
        result = executoer_for_web_server(pname, cardNum)

        return json_dumps(result)




application = tornado.web.Application([(r"/pste", MainHandler),])


if __name__ == "__main__":
    application.listen(22000)
    IOLoop.instance().start()
