#coding: utf-8
from socket import *
from work.log import log
logger = log.logger
from config import setting
import entry
import json
import model
from hashlib import md5
import re

### Url mappings
web = setting.web
config = setting.config
web.config.debug = config.debug
render = setting.render
render2 = setting.render2
db = setting.db
session = setting.session

class CookieSet:
    def GET(self):
        i = web.input(user='guest')
        web.setcookie('user', i.user, 3600)
        return "Age set in your cookie"

class CookieGet:
    def GET(self):
        c = web.cookies(user="guest")
        return "Your name is: " + c.user

class Base:
    def GET(self):
        if session.login:
            return render2.base2()
        else:
            return render2.login()

def logged():
    if session.login==1:
        return True
    else:
        return False

class Login:
    def GET(self):
        if logged():
            return render2.base2()
        else:
            return "%s" % (
                render2.login()
                )
    def POST(self):
            user, passwd = web.input().user, web.input().passwd
            ident = db.query("select * from example_users where user = '%s'" % (user))
            ident = dict(ident[0]).copy()
            passwd =md5(passwd).hexdigest()
            try:
                if passwd == ident['pass']:
                    session.login=1
                    session.privilege=ident['privilege']
                    return render2.base2()
                else:
                    session.login=0
                    session.privilege=0
                    return "%s" % (
                        'User Or Passwd ERROE'
                        )
            except Exception, e:
                logger.error(e)
                session.login=0
                session.privilege=0
                return "%s" % (
                    'ERROR'
                    )
class reset:
    def GET(self):
        session.login=0
        session.kill()
        return "%s" % (
            render2.login()
            )

html_data = dict()
class Pagerule:
    def GET(self):
        return render.pagerule()
    def POST(self):
        global html_data
        form = web.input()
        view_data = entry.get_page_view_data(form)
        data = entry.get_page_html(view_data)
        #view_data['info']['dominfo'] = data.get('dominfo', '')
        html_data = data.get('dominfo', '')
        for s in data:
            if data['flag'] == 'SUC':
                html = '''<h3 align="center">%s</h3>
                        <p style="padding:15px 0 1px;font-size:15px">来源:%s</p>
                        <p>日期:%s</p>
                        <div id="side-content"><br><br>%s</div>
                        ''' % (data['title'], data.get('contentSource', ''),
                                data.get('date', ''), data['content'])
            else:
                html = '''<h2>%s</h2>
                        <p>INFO:%s</p>''' % (data.get('title', 'no title'), data['flag'])
        return json.dumps(html)

class Cmpagerule:
    def POST(self):
        try:
            global html_data
            form = web.input()
            view_data = entry.get_page_view_data(form)
            view_data['info']['dominfo'] = html_data

            del view_data['view'], view_data['info']['imgorstr'], view_data['info']['layer'], view_data['info']['ImgOrLev']

            view_data['url'] = view_data['re_url']
            del view_data['re_url']
            view_data['info'] = json.dumps(view_data['info'])
            model.insert_url_extraction(view_data)
            return '规则入库成功'
        except KeyError,reason:
            logger.error(str(reason))
            return '请先预览成功后，再提交'

beings_data = dict()
class Beingsrule:
    def GET(self):
        return render.beingsrule()
    def POST(self):
        global beings_data
        form = web.input()
        form.view = 'formulate'
        form.filtration = '%s;&xg&;%s;&xg&;%s' % (form.filter_tag, form.filter_attr, form.filter_text)
        data = entry.get_topic_html(form)
        if data[0] is False:
            string='''%s''' % data[1]
            beings_data = False
        else:
            form.url_md5 = md5(form.url).hexdigest()
            form.content_start = json.dumps({'filtration':form.filtration, 'dominfo':data[0][0]})
            beings_data = data[0][0]
            #beings_data = dict(form)

            string = '''<table class="tabmain">
                                <thead>
                                    <tr>
                                        <th>序号</th>
                                        <th>内容</th>
                                    </tr>
                                </thead><tbody>'''

            for t,s in enumerate(data[0][1]):
                tmp = 'alt-row' if t%2 == 0 else ''
                string +=''' <tr align="center" class="datarow %s">
                        <td class="tt">%s</td>
                        <td> <a href="%s">%s</a></td>
                    </tr>''' % (tmp, t + 1, s[0], s[1])
            string += '</tbody></table>'
        return json.dumps(string)

class Cmbeingsrule:
    def POST(self):
        try:
            global beings_data

            if beings_data is False:
                return '预览不成功，无法提交'

            form = web.input()
            form.filtration = '%s;&xg&;%s;&xg&;%s' % (form.filter_tag, form.filter_attr, form.filter_text)
            form.url_md5 = md5(form.url).hexdigest()
            form.content_start = json.dumps({'filtration':form.filtration, 'dominfo':beings_data})

            result = dict(form)

            if result is False:
                return '预览不成功，无法提交'
            del result['filtration'], result['string'], result['filter_tag'], result['filter_attr'], result['filter_text']
            result = model.insert_beings_spider(result)
            if result == 1062:
                return '入库失败，请在url末尾添加"#1"或"#2"...'
            elif result != [0]:
                return 'error: result'

            return '规则入库成功'
        except KeyError,reason:
            logger.error(str(reason))
            return '请先预览成功后，再提交'


class Editpagerulebyid:

    def organize(self, data):
        data = web.storify(dict(data))
        info = json.loads(data.info)
        filtration = info['filtration']
        data.imgreplace = info.get('imgreplace', '')

        filterinfo, filtertext = unpack(filtration)
        data.filter_tag = ''
        data.filter_attr = ''
        if len(filtertext)%2 == 1:
            filtertext.append('')
        data.filter_text = filtertext
        data.filter_text_num = len(filtertext)
        if len(filterinfo) == 2:
            data.filter_tag = filterinfo[0]
            data.filter_attr = filterinfo[1]
        return data

    def GET(self, id):
        form = model.select_url_extraction_id(id)
        data = self.organize(form[0])
        return render.editpagerulebyid(data)

    def POST(self, id):
        data = web.input()
        filtration = '%s;&xg&;%s' % (data.filter_tag, data.filter_attr)
        for i in range(0, int(data.filter_text_num), 2):
            filtration += ';&xg&;%s;&xg&;%s' % (eval('data.filter_textstart_%s' % i), eval('data.filter_textend_%s' % (i + 1)))
        info = json.loads(data.info)
        info['filtration'] = filtration
        info['imgreplace'] = data.get('imgreplace', '')

        data.info = json.dumps(info)
        model.update_url_extraction(id, data)
        form = model.select_url_extraction_id(id)
        data = self.organize(form[0])
        return render.editpagerulebyid(data)

def unpack(filtration):
    try:
        filterinfo = []
        filtertext = ['']
        if not re.sub('\$', '', filtration) or not re.sub(';&xg&;', '', filtration):
            pass
        else:
            #filtration = re.sub('\*\$', '**', filtration)
            if ';&xg&;'  in filtration:
                part = filtration.split(';&xg&;')
            else:
                part = filtration.split('$$')
            filterinfo.append(part[0])
            filterinfo.append(part[1])
            if len(part) > 2:
                filtertext = part[2:]
        return filterinfo, filtertext
    except Exception, e:
        logger.error(e)
        return False

class Editbeingsrulebyurlmd:
    def organize(self, data):
        data = web.storify(dict(data))
        content_start= json.loads(data.content_start)
        filtration = content_start['filtration']
        data.dominfo = content_start['dominfo']

        filterinfo, filtertext = unpack(filtration)
        data.filter_tag = ''
        data.filter_attr = ''
        data.filter_text = filtertext[0]
        if len(filterinfo) == 2:
            data.filter_tag = filterinfo[0]
            data.filter_attr = filterinfo[1]
        return data

    def GET(self, data):
        url_md5, beings_id = data.split('&')
        #url_md5_ = data.get('url_md5', None)
        #print url_md5_, 222
        #if url_md5_:
            #url_md5 = url_md5_

        form = model.select_beings_spider_urlmd(url_md5, beings_id)
        if form:
            data = self.organize(form[0])
            return render.editbeingsrulebyurlmd(data)
        else:
            return '找不到页面'
    def POST(self, info):
        #print data
        data = web.input()
        print data
        #url_md5 = data.get('url_md5')
        #ori_beings_id = data.get('beings_id')
        url_md5, ori_beings_id = info.split('&')
        url_md5_ = data.get('url_md5', None)
        if url_md5_:
            url_md5 = url_md5_

        filtration = '%s;&xg&;%s;&xg&;%s' % (data.filter_tag, data.filter_attr, data.filter_text)
        data.content_start = json.dumps({'filtration':filtration, 'dominfo':data.dominfo})
        #print data

        new_url_md5 = md5(data.url).hexdigest()
        data.url_md5 = new_url_md5
        model.update_beings_spider(url_md5, ori_beings_id, data)
        form = model.select_beings_spider_urlmd(new_url_md5, data.beings_id)
        if form:
            response = self.organize(form[0])
            response.url_md5 = new_url_md5
            return render.editbeingsrulebyurlmd(response)
        else:
            return '找不到页面'

class Editpagerule:
    def GET(self):
        params = web.input()
        page = int(params.get('page', 1))
        if page < 1: page = 1
        domain = params.get('domain', '')
        query = params.get('query', '')
        if query == 'regular':
            regular_url = params.get('regular_url', '')
            domain_url = params.get('domain', '')

            if not regular_url or not domain_url:
                pass

            domain_data = model.get_regular_by_domain(domain_url)
            posts = []
            if domain_data:
                for domain_regular in domain_data:
                    #domain_regular_temp = domain_regular
                    if  re.compile(domain_regular.url).search(regular_url):
                        posts.append(domain_regular)
            else:
                posts = ''

            return render.editpagerule(nums=len(posts), posts=posts, page=1, pages=[1,2,3,4,5],total=1,lastpage=1,nextpage=1, domain='', regular_url=regular_url)
        else:
            perpage = 25
            postcount = model.select_count_url_extraction(domain)
            pages = postcount.count / perpage
            mod = postcount.count % perpage

            if mod > 0:
                pages += 1

            if page > pages:
                page = pages

            offset = (page - 1) * perpage

            posts = model.select_url_extraction_domain(offset, perpage, domain)

            lastpage=int(page)-1
            nextpage=int(page)+1
            '''page3, 分页，默认5页'''
            page3=[page -2, page-1, page, page + 1, page + 2]
            '''page3, 分页，前两页特殊情况'''
            if page == 1:
                page3 = [1,2,3,4,5]
            elif page == 2:
                page3 = [1,2,3,4,5]

            return render.editpagerule(nums=postcount.count, posts=posts, page=page,pages=page3,total=pages,lastpage=lastpage,nextpage=nextpage, domain=domain, regular_url='')

class Editbeingsrule:
    def GET(self):
        params = web.input()
        page = int(params.get('page', 1))
        if page < 1: page = 1
        string = params.get('string', '')

        perpage = 25
        postcount = model.select_count_beings_spider(string)
        count = postcount.count
        pages = postcount.count / perpage
        mod = postcount.count % perpage

        if mod > 0:
            pages += 1

        if page > pages:
            page = pages

        offset = (page - 1) * perpage

        posts = model.select_beings_spider(offset, perpage, string)
        if posts is False:
            posts = False
            count = 0

        lastpage=int(page)-1
        nextpage=int(page)+1
        '''page3, 分页，默认5页'''
        page3=[page -2, page-1, page, page + 1, page + 2]
        '''page3, 分页，前两页特殊情况'''
        if page == 1:
            page3 = [1,2,3,4,5]
        elif page == 2:
            page3 = [1,2,3,4,5]

        return render.editbeingsrule(nums=count, posts=posts, page=page,pages=page3,total=pages,lastpage=lastpage,nextpage=nextpage, string=string)


class Delpagerulebyid:
    def POST(self):
        data = web.input()
        id = data.id
        result = model.del_url_extraction(id)
        if type(result) is long :
        #if result == 1:
            msg = "删除成功"
        else:
            msg = "删除失败"
        return msg
class Delbeingsrulebyurlmd:
    def POST(self):
        data = web.input()
        url_md5= data.url_md5
        beings_id = data.beings_id
        result = model.del_beings_spider(url_md5, beings_id)
        if type(result) is long :
        #if result == 1:
            msg = "删除成功"
        else:
            msg = "删除失败"
        return msg
class Gethtml:
    def GET(self):
        return render.gethtml()

class Crawlbyid:
    def POST(self):
        data = web.input()
        result = entry.crawl_by_id(data)
        if result[0] is False:
            string = '<br><p>%s</p>' % result[1]
        else:
            string = '''<table class="tabmain">
                                    <thead>
                                        <tr>
                                            <th>序号</th>
                                            <th>doingsid</th>
                                            <th>title</th>
                                            <th>result</th>
                                        </tr>
                                    </thead><tbody>'''

            for t,s in enumerate(result):
                tmp = 'alt-row' if t % 2 == 0 else ''
                string +=''' <tr align="center" class="datarow %s">
                        <td class="tt">%s</td>
                        <td> <a href="http://in-beta.xianguo.com/doing/%s">%s</a></td>
                        <td class="tt">%s</td>
                        <td class="tt">%s</td>
                    </tr>''' % (tmp, t + 1, s['url'], s['id'],s['title'], s['flag'])
            string += '</tbody></table>'

        return string

class Beingsmanage:
    def GET(self):
        params = web.input()
        page = int(params.get('page', 1))
        if page < 1: page = 1
        beings_id= params.get('beings_id', '')

        perpage = 20
        postcount = model.select_count_beings(beings_id)
        count = postcount.count
        if not beings_id:
            '''all'''
            pages = postcount.count // perpage
            mod = postcount.count % perpage
            if mod > 0:
                pages += 1
        else:
            pages = 1

        if page > pages:
            page = pages

        offset = (page - 1) * perpage

        posts = model.select_beings(offset, perpage, beings_id)
        if posts is False:
            count = 0
            posts = False
        lastpage=int(page)-1
        nextpage=int(page)+1
        '''page3, 分页，默认5页'''
        page3=[page -2, page-1, page, page + 1, page + 2]
        '''page3, 分页，前两页特殊情况'''
        if page == 1:
            page3 = [1,2,3,4,5]
        elif page == 2:
            page3 = [1,2,3,4,5]

        return render.beingsmanage(nums=count, posts=posts, page=page,pages=page3,total=pages,lastpage=lastpage,nextpage=nextpage, beings_id=beings_id)
class Delbeings:
    def POST(self):
        data = web.input()
        id = data.id
        mode = data.mode
        result = model.del_beings(id, mode)
        if type(result) is long :
            msg = "删除成功"
        else:
            msg = "删除失败"
        return msg

class Addbeings:
    def POST(self):
        data = web.input()
        beings_id = data.beings_id
        result = model.add_beings(beings_id)
        if type(result) is long:
            msg = "新增成功"
        else:
            msg = "新增失败"
        return msg
class Diybeings_crawl:
    def POST(self):
        """docstring for POST"""
        # TODO: write code...
        data = web.input()
        beings_id = data.beings_id
        url = data.url
        result = entry.diybeings_crawl(beings_id, url)
        return result

class Beings_preview:
    def POST(self):
        data = web.input()
        url =data.url
        content_start = data.content_start
        data = entry.beings_preview(url, content_start)

        if data[0] is False:
            string='''<br><div style="color: white;font-size:15px;"><p>%s</p></div>''' % data[1]
        else:
            string = '''<table class="tabmain">
                                <thead>
                                    <tr>
                                        <th>序号</th>
                                        <th>内容</th>
                                    </tr>
                                </thead><tbody>'''

            for t,s in enumerate(data[0][1]):
                tmp = 'alt-row' if t%2 == 0 else ''
                string +=''' <tr align="center" class="datarow %s">
                        <td class="tt">%s</td>
                        <td> <a href="%s">%s</a></td>
                    </tr>''' % (tmp, t + 1, s[0], s[1])
            string += '</tbody></table>'
        return json.dumps(string)

class Urltest:
    def GET(self):
        return render.urltest()
    def POST(self):
        data = web.input()
        url = data.get('url', '')
        if not url:
            html = '''<h2>%s</h2>
                    ''' % ("请输入URL")
        else:
            data = self.sockercode(url)

            if data['flag'] == 'SUC':
                html = '''<h3 align="center">%s</h3>
                        <p style="padding:15px 0 1px;font-size:15px">来源:%s</p>
                        <div id="side-content"><br><br>%s</div>
                        ''' % (data['title'], '' if data.get('contentSource', None) is None
                                else data['contentSource'], data['content'])
            else:
                html = '''<h2>%s</h2>
                        <p>INFO:%s</p>''' % (data.get('title', 'no title'), data['flag'])
        return json.dumps(html)

    def sockercode(self,url):
        HOST = '192.168.123.6'
        PORT = 21568
        ADDR = (HOST, PORT)
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

        test = {'url':url.strip()}
        test = json.dumps(test)
        tcpCliSock.send(test)
        data =tcpCliSock.recv(300000)
        data = json.loads(data)
        #for k in data:
            #print k, data[k].encode('utf-8')
        tcpCliSock.close()
        return data
