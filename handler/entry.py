#coding: utf-8
import re
import requests
import socket
from topicwork.runphp.classes import  RunPhp_Being
import json
from work.encode.encoding import get_encoding
import jspagedeal
from topicwork.assignzone import topicview
from work.public.paging import getcontent_serverside
import urllib2
def get_page_view_data(form):
    url = form.url
    mode = int(form.ext_mode)
    paging = int(form.paging_mode)
    view = 0
    info = {}
    string = ''

    ';&xg&; as delimiter'
    for i in range(int(form.filter_text_num)):
        i += 1
        string += ';&xg&;%s;&xg&;%s' % (eval('form.filter_textstart_%s' % i), eval('form.filter_textend_%s' % i))

    info['filtration'] = '%s;&xg&;%s%s' % (form.filter_tag, form.filter_attr, string)
    info['sourcemode'] = form.source_mode
    info['soutag'] = form.source_tag
    info['souattr'] = form.source_attr
    info['soucon'] = form.source_con
    info['soutext'] = form.source_text
    info['imgorstr'] = form.img
    info['ImgOrLev'] = 1
    info['layer'] = form.layer
    info['tag'] = form.paging_tag
    info['attr'] = form.paging_attr
    info['con'] = form.paging_con
    info['imgreplace'] = form.img_src
    render = form.render
    data = {'name': form.name, 'url': url, 'mode':mode, 'paging':paging, 'view':view, 'info':info, 'js':render, 'domain': form.domain, 're_url': form.re_url}
    return data

def get_page_html(data):
    url = data['url']
    file = get_file(url)
    #file = urllib2.urlopen(url, timeout=10).read()
    data = getcontent_serverside(url, data['mode'], data['js'],
                    data['paging'], data['info'], data['view'], file)
    return data

def get_topic_view_data(form):
    pass
def get_file_bak(url, js=None):
    if js and  'js' in js[0]:
        file = jspagedeal.getpage(url)
    else:
        req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0"})
        response = urllib2.urlopen(req, timeout = 15)
        #get real url
        file = response.read()
    return file


def get_file(url, js=None):
    if js and  'js' in js[0]:
        file = jspagedeal.getpage(url)
    else:
        req = requests.get(url, headers={'User-Agent' : "fake-clients"})
        #get real url
        file = req.content
    return file

def get_topic_html(data):
    '''beings强抓:获取url list'''
    url = data.url
    string = data.string
    view = data.view
    filtration = data.filtration
    try:
        p = re.compile(r'#(.*$)')
        js = p.findall(url)
        url = re.sub('#.*$', '', url)
        file = get_file(url, js)
    except Exception, e:
        return False,e

    coding = get_encoding(file)
    if coding is None:
        return False, 'get coding error'
    if view == 'preview':
        return topicview.GetUrl(url, file, coding, string, filtration).previewrule()
    elif view == 'formulate':
        return topicview.GetUrl(url, file, coding, string, filtration).formulaterule()

def crawl_by_id(data):
    '''mode:1按照beingsid抓取, 2:按照doingsid抓取'''
    url = 'http://in-api.xianguo.com/i/inside/doingsedit.json'
    mode = data.ext_mode
    try:
        if int(mode) == 1:
            url = url + '?beings_id=%s' % data.beingsid
            if data.crawl_num:
                url += '&count=%s' % data.crawl_num
            else:
                url += '&count=20'

            if data.start_doingsid:
                url += '&max_id=%s' % data.start_doingsid
            print url
            file = urllib2.urlopen(url, timeout=120).read()
            print file
            if file:
                return json.loads(file)['list']
            else:
                return [False, '无法抓取']
        else:
            url = url + '?doings_id=%s' % (data.doingsid)
            file = urllib2.urlopen(url, timeout=120).read()
            if file:
                return json.loads(file)['list']
            else:
                return [False, '抓取失败，失败原因查看日志']
    except socket.timeouterror, e:
        return False, '接收超时，但并不意味着抓取不成功'

def diybeings_crawl(beings_id, url):
    result = RunPhp_Being(url, beings_id).getmultiurls()
    return
def beings_preview(url, content_start):
    """docstring for beings_preview"""
    # TODO: write code...
    data = json.loads(content_start)
    string = data['dominfo']
    view = "preview"
    filtration = data['filtration']
    try:
        p = re.compile(r'#(.*$)')
        js = p.findall(url)
        url = re.sub('#.*$', '', url)
        file = get_file(url, js)
    except Exception, e:
        return False,e

    coding = get_encoding(file)
    if coding is None:
        return False, 'get coding error'
    if view == 'preview':
        return topicview.GetUrl(url, file, coding, string, filtration).previewrule()
    elif view == 'formulate':
        return topicview.GetUrl(url, file, coding, string, filtration).formulaterule()


