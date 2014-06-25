#coding: utf-8
import json
import random
import tornado.web
from crawlsystem.extractwork.utils import getCoding
from crawlsystem.extractwork.extract import getRssContent
from crawlsystem.model import DButils
import tornado.escape
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
import tornado.gen
import config
import hashlib
cache = config.cache
logger = config.logger
class RssRuleHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render('rssrule.html', )

    @tornado.gen.coroutine
    def post(self):
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
        if url:
            client = AsyncHTTPClient()
            print url
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

            self.finish(tornado.escape.json_encode(result))

class RssRuleViewHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        name = self.get_argument('name')
        url = self.get_argument('rss_url')
        ftags = self.get_argument('tags').split('|')
        fclasses = self.get_argument('classes').split('|')
        ftext = self.get_argument('text')
        maintext = self.get_argument('maintext')
        result = dict()
        logger.info(maintext)

        if url:
            client = AsyncHTTPClient()
            urlrequest = HTTPRequest(url, connect_timeout=5, request_timeout=12)
            response = yield tornado.gen.Task(client.fetch, urlrequest)

            url = response.effective_url

            crawl_info = dict(maintext=maintext,
                              filterdominfo=dict(filtertag=ftags,
                                                 filterclass=fclasses),
                              filterhtmlinfo=dict(ftext=ftext))

            if response.code == 200:
                coding = getCoding(response.body)
                body = response.body.decode(coding, 'ignore')
                result = getRssContent(url, body, crawl_info)
                content = result.get('content')
                if content:
                    taginfo = result.get('taginfo')
                    order = result.get('order')
                    str1 = '''
                                <table class="table">
                                <thead>
                                    <tr>
                                    <th>num</th>
                                    <th>title</th>
                                    </tr>
                                </thead>
                                <tbody>'''
                    for num, (link, title) in enumerate(content):
                        print num, title, link
                        str1 += '''
                                    <tr>
                                        <td>%s</td>
                                        <td><a href="%s">%s</a></td>
                                    </tr>
                                ''' % (num + 1, link, title)
                    str1 += ' </tbody> </table>'


        htmls = str1
        url_md5 = hashlib.md5(url + str(random.randint(100000,999999))).hexdigest().upper()
        cache.set(url_md5, htmls)
        cache.set(url_md5 + 'dominfo', dict(taginfo=taginfo, order=order))
        self.finish(url_md5)


class RssRuleContentHandler(tornado.web.RequestHandler):
    def get(self):
        url_md5 = self.get_argument('url_md5', None)
        loading = self.get_argument('loading', None)
        htmls = ''
        if loading == '1':
            htmls = '''<img src="/static/img/loading.gif">'''
        if url_md5:
            htmls = cache.get(url_md5)
        self.finish(htmls)

class RssRuleCommitHandler(tornado.web.RequestHandler):
    #@tornado.gen.coroutine
    def post(self):
        name = self.get_argument('name')
        url = self.get_argument('rss_url')
        ftags = self.get_argument('tags').split('|')
        fclasses = self.get_argument('classes').split('|')
        ftext = self.get_argument('text')
        urlmd5 = self.get_argument("urlmd5")
        dominfo = eval(cache.get(urlmd5 + 'dominfo'))
        res= '1'
        if urlmd5:
            crawl_info = dict(dominfo=dominfo,
                              filterdominfo=dict(filtertag=ftags,
                                                 filterclass=fclasses),
                              filterhtmlinfo=dict(ftext=ftext))
            info = dict(url=url,
                        name=name,
                        crawl_info=json.dumps(crawl_info))
            logger.info(info)
            res = DButils.writeRssInfo(info)
        self.finish(res)


class RssAdminCommitHandler(tornado.web.RequestHandler):
    def get(self):
        string = self.get_argument('string', None)
        result = DButils.readRssInfo(string)
        logger.info(result)
        return self.render('rssadmin.html', data=result)
