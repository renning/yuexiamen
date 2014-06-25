#coding: utf-8
import json
import tornado.web
from crawlsystem.extractwork.utils import getCoding
from crawlsystem.extractwork.extract import getPageContent
import tornado.escape
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from crawlsystem.model import DButils
import tornado.gen
import config
import hashlib
logger = config.logger
cache = config.cache
class ReadRuleHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render('readrule.html', )

class ReadRuleViewHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        name = self.get_argument('name')
        url = self.get_argument('url')
        paging = self.get_argument('optionsRadios')
        nextpagename = self.get_argument('nextpagename')
        ftags = self.get_argument('tags').split('|')
        fclasses = self.get_argument('classes').split('|')
        fimgurl = self.get_argument('imgurl')
        ftext1start = self.get_argument('text1start')
        ftext1end = self.get_argument('text1end')
        ftext2start = self.get_argument('text2start')
        ftext2end = self.get_argument('text2end')
        imgreplace= self.get_argument('imgreplace', '')
        filtertext = [[ftext1start, ftext1end], [ftext2start, ftext2end]]
        result = dict()

        if url:
            client = AsyncHTTPClient()
            urlrequest = HTTPRequest(url, connect_timeout=5, request_timeout=12)
            response = yield tornado.gen.Task(client.fetch, urlrequest)

            logger.info(response)
            url = response.effective_url

            crawl_info = dict(crawl_mode=1,
                              paging_mode=int(paging),
                              nextpageinfo=dict(tagname='a',
                                                attr='text',
                                                con=nextpagename),
                              filterdominfo=dict(filterimg=fimgurl,
                                                 filtertag=ftags,
                                                 filterclass=fclasses),
                              filterhtmlinfo=dict(filtertext=filtertext,
                                                  imgreplace=imgreplace),
                              sourceinfo=dict())

            if response.code == 200:
                coding = getCoding(response.body)
                body = response.body.decode(coding, 'ignore')

                content = getPageContent(url, body, crawl_info, first_page=True)
                result = content
                print result.keys()
                print result['title']

                next_pages = content.get('next_pages')
                print 'next_pages', next_pages

                if next_pages:
                    while True:
                        if isinstance(next_pages, list):
                            if next_pages:
                                next_page_url = next_pages.pop(0)
                            else:
                                break
                        elif not next_page_url:
                            break

                        response = yield tornado.gen.Task(client.fetch, next_page_url)
                        if response.code == 200 and response.body:
                            url = response.effective_url
                            body = response.body.decode(coding, 'ignore')
                            result = getPageContent(url, body, crawl_info)
                            print 444,  result.keys()
                            next_page_url = result.get('next_pages')
                        else:
                            break
        htmls = '''<h2>%s</h2><p>返回码:%s</p> %s''' % (result.get('title'), response.code, result.get('content'))
        url_md5 = hashlib.md5(url).hexdigest().upper()
        cache.set(url_md5, htmls)
        self.finish(url_md5)

class RuleContentHandler(tornado.web.RequestHandler):
    def get(self):
        url_md5 = self.get_argument('url_md5', None)
        loading = self.get_argument('loading', None)
        htmls = ''
        if loading == '1':
            htmls = '''<img src="/static/img/loading.gif">'''
        if url_md5:
            htmls = cache.get(url_md5)
        self.finish(htmls)

class ReadRuleCommitHandler(tornado.web.RequestHandler):
    #@tornado.gen.coroutine
    def post(self):
        name = self.get_argument('name')
        url_example = self.get_argument('url')
        domain = self.get_argument('domain', "")
        url_regular = self.get_argument('url_regular', "")
        paging = self.get_argument('optionsRadios')
        nextpagename = self.get_argument('nextpagename')
        ftags = self.get_argument('tags').split('|')
        fclasses = self.get_argument('classes').split('|')
        fimgurl = self.get_argument('imgurl')
        ftext1start = self.get_argument('text1start')
        ftext1end = self.get_argument('text1end')
        ftext2start = self.get_argument('text2start')
        ftext2end = self.get_argument('text2end')
        imgreplace= self.get_argument('imgreplace', '')
        filtertext = [[ftext1start, ftext1end], [ftext2start, ftext2end]]

        crawl_info = dict(crawl_mode=1,
                            paging_mode=int(paging),
                            nextpageinfo=dict(tagname='a',
                                            attr='text',
                                            con=nextpagename),
                            filterdominfo=dict(filterimg=fimgurl,
                                                filtertag=ftags,
                                                filterclass=fclasses),
                            filterhtmlinfo=dict(filtertext=filtertext,
                                                imgreplace=imgreplace),
                            sourceinfo=dict())
        info = dict(url_example=url_example,
                    url_regular=url_regular,
                    name=name,
                    domain=domain,
                    crawl_info=json.dumps(crawl_info))
        res = DButils.writeRuleInfo(info)
        print res
        self.finish(res)
class DoveRuleHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render('doverule.html', )

class DoveRuleViewHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        print self.request.body
        name = self.get_argument('name')
        url = self.get_argument('url')
        paging = self.get_argument('optionsRadios')
        nextpagename = self.get_argument('nextpagename')
        tags = self.get_argument('tags')
        classes = self.get_argument('classes')
        imgurl = self.get_argument('imgurl')
        text1start = self.get_argument('text1start')
        text1end = self.get_argument('text1end')
        text2start = self.get_argument('text2start')
        text2end = self.get_argument('text2end')
        result = dict()
        if url:
            client = AsyncHTTPClient()
            response = yield tornado.gen.Task(client.fetch, url)

            url = response.effective_url

            crawl_info = dict(crawl_mode=1)
            coding = getCoding(response.body)
            body = response.body.decode(coding, 'ignore')

            content = getPageContent(url, body, crawl_info, first_page=True)
            result = content
            next_pages = content.get('next_pages')

            if next_pages:
                while True:
                    if isinstance(next_pages, list):
                        if next_pages:
                            next_page_url = next_pages.pop(0)
                        else:
                            break
                    elif not next_page_url:
                        break

                    response = yield tornado.gen.Task(client.fetch, next_page_url)
                    if response.code == 200 and response.body:
                        url = response.effective_url
                        body = response.body.decode(coding, 'ignore')
                        result = getPageContent(url, body, crawl_info)
                        print result
                        next_page_url = result.get('next_pages')
                    else:
                        break
        htmls = '''<h2>%s</h2> %s''' % (result.get('title'), result.get('content'))
        url_md5 = hashlib.md5(url).hexdigest().upper()
        cache.set(url_md5, htmls)
        self.finish(url_md5)

class DoveRuleContentHandler(tornado.web.RequestHandler):
    def get(self):
        url_md5 = self.get_argument('url_md5', None)
        loading = self.get_argument('loading', None)
        htmls = ''
        if loading == '1':
            htmls = '''<img src="/static/img/loading.gif">'''
        if url_md5:
            htmls = cache.get(url_md5)
        self.finish(htmls)

class DoveRuleCommitHandler(tornado.web.RequestHandler):
    #@tornado.gen.coroutine
    def post(self):
        name = self.get_argument('name')
        url_example = self.get_argument('url')
        domain = self.get_argument('domain', "")
        url_regular = self.get_argument('url_regular', "")
        paging = self.get_argument('optionsRadios')
        nextpagename = self.get_argument('nextpagename')
        ftags = self.get_argument('tags').split('|')
        fclasses = self.get_argument('classes').split('|')
        fimgurl = self.get_argument('imgurl')
        ftext1start = self.get_argument('text1start')
        ftext1end = self.get_argument('text1end')
        ftext2start = self.get_argument('text2start')
        ftext2end = self.get_argument('text2end')
        imgreplace= self.get_argument('imgreplace', '')
        dominfo = self.get_argument("dominfo", "")
        filtertext = [[ftext1start, ftext1end], [ftext2start, ftext2end]]

        crawl_info = dict(crawl_mode=1,
                            paging_mode=int(paging),
                            dominfo=dominfo,
                            nextpageinfo=dict(tagname='a',
                                            attr='text',
                                            con=nextpagename),
                            filterdominfo=dict(filterimg=fimgurl,
                                                filtertag=ftags,
                                                filterclass=fclasses),
                            filterhtmlinfo=dict(filtertext=filtertext,
                                                imgreplace=imgreplace),
                            sourceinfo=dict())
        info = dict(url_example=url_example,
                    url_regular=url_regular,
                    name=name,
                    domain=domain,
                    crawl_info=json.dumps(crawl_info))
        res = DButils.writeRuleInfo(info)
        print res
        self.finish(res)

