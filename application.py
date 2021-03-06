#coding:utf-8

import tornado.web
import os
from handler.login import *
from handler.mudidi import *
import Settings

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/auth/login/", AuthLoginHandler),
            (r"/auth/logout/", AuthLogoutHandler),
            (r"/auth/logout/", AuthLogoutHandler),
            (r"/auth/logout/", AuthLogoutHandler),
            (r"/mudidi/", MudidiHandler),
            (r"/add/place/(\d+)/(.*)/(\d+)/(.*)/", ChildPlaceAddHandler),
            (r"/add/place/(\d+)/(.*)/", PlaceAddHandler),
            (r"/add/poi/(\d+)/(.*)/", PoiAddHandler),
            (r"/add/featured/(\d+)/(.*)/", FeaturedAddHandler),
            (r"/add/raiders/(\d+)/(.*)/", RaidersAddHandler),
            (r"/poiadmin/(\d+)/(.*)/", PoiadminHandler),
            (r"/poi/(\d+)/(.*)/", PoiHandler),
            (r"/place/(\d+)/(.*)/", PlaceHandler),
            #(r"/poi/(\d+)/(.*)/", PoiHandler),
        ]
        settings = {
            "template_path":Settings.TEMPLATE_PATH,
            "static_path":Settings.STATIC_PATH,
            "debug":Settings.DEBUG,
            "cookie_secret": Settings.COOKIE_SECRET,
            "login_url": "/auth/login/"
        }
        tornado.web.Application.__init__(self, handlers, **settings)
