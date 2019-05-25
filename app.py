#!/usr/bin/python
# -*- coding: utf-8 -*


import tornado.ioloop
import tornado.web
from tornado.options import define,options
from handlers import main

# 定义端口信息
define('port',default=8888,type=int,help="Listening port")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", main.IndexHandler),
            (r"/signup", main.SignupHandler),
            (r"/changep", main.ChangePHandler),
            (r"/login", main.LoginHandler),
            (r"/explore", main.ExploreHandler),
            (r"/upload", main.UploadHandler),
            (r"/exit", main.Exit1Handler),
            # 命令捕获
            # (?P < post_id >[0-9]+) 捕获输入的id值传入到post_id中
            (r"/post/(?P<post_id>[0-9]+)", main.PostHandler),
        ]
        settings = dict(
            debug=True,
            template_path='templates',
            static_path='statics',
            cookie_secret='suiyishuruzifuchuan12345643sadgsjg;;?al',  # cookie_secret用户自定义
            login_url='/login',
            xsrf_cookies=True,
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                    # 'password': '',
                    'db_sessions': 5,  # redis db index
                    # 'db_notifications': 11,
                    'max_connections': 2 ** 30,
                },
                'cookies': {
                    'expires_days': 30,
                },
            }
        )
        # 继承父类的init，主要起作用的是父类的init
        super().__init__(handlers=handlers,**settings)


if __name__ == '__main__':
    app = Application()
    # 命令行参数转换
    # eg:[I 190511 23:29:49 web:2246] 304 GET / (192.168.32.1) 1.57ms
    tornado.options.parse_command_line()
    app.listen(options.port)
    print("Server start on port {}".format(options.port))
    tornado.ioloop.IOLoop.current().start()
    # 命令行输入python app.py - -port = 8001 web将运行在8001端口


