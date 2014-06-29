#coding: utf-8
import tornado.ioloop
from application import Application
from tornado.httpclient import AsyncHTTPClient
from tornado.options import define, options
AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')


define("port", default=8080, help="run on the given port", type=int)
if __name__ == '__main__':
    #tornado.options.parse_command_line()
    #application.listen(options.port)
    #tornado.ioloop.IOLoop.instance().start()
     tornado.options.parse_command_line()
     http_server = tornado.httpserver.HTTPServer(Application())
     http_server.listen(options.port)
     tornado.ioloop.IOLoop.instance().start()
    #application = tornado.web.Application([
            #(r"/getpagebody", GetPageBodyControl),
            #], debug=False)
    #http_server = httpserver.HTTPServer(application)
    #http_server.bind(options.port)
    #http_server.start(0)
    #tornado.ioloop.IOLoop.instance().start()
