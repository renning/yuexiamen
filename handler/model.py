#coding: utf-8
import time
from config import setting
db = setting.db
db2 = setting.db2

def get_regular_by_domain(domain):
    try:
        if domain is not None:
            data = db.query('select * ,from_unixtime(create_time) as time1, from_unixtime(update_time) as time2 from url_extraction where domain="%s" order by create_time desc ' % domain , vars = locals())
        else:
            data = db.query('select * ,from_unixtime(create_time) as time1, from_unixtime(update_time) as time2 from url_extraction where domain is NULL or domain="" order by create_time desc ' , vars = locals())
        return data
    except Exception, e:
        return False

def insert_url_extraction(html_data):
    html_data['create_time'] = int(time.time())
    db.multiple_insert('url_extraction', values=[html_data])

def insert_beings_spider(beings_data):
    try:
        print beings_data
        beings_data['create_time'] = int(time.time())
        return db2.multiple_insert('tg_beings_spider', values=[beings_data])
    except Exception, e:
        print e
        return e[0]

def select_url_extraction_id(id = None):
    try:
        if id:
            form = db.select('url_extraction', where="id=$id", vars = locals())
        else:
            #form = db.select('url_extraction', vars = locals())
            form = db.query('select * ,from_unixtime(create_time) as time1, from_unixtime(update_time) as time2 from url_extraction order by create_time')
        return form
    except Exception, e:
        return False

def select_beings_spider_urlmd(url_md5 = None, ori_beings_id=None):
    try:
        if url_md5:
            form = db2.select('tg_beings_spider', where="url_md5=$url_md5 and beings_id=$ori_beings_id", vars = locals())
        else:
            form = db2.query('select * ,from_unixtime(create_time) as time1, from_unixtime(update_time) as time2 from tg_beings_spider order by create_time')
        return form
    except Exception, e:
        print e
        return False
def select_url_extraction_domain(offset, perpage, domain = ''):
    try:
        form = db.query('select * ,from_unixtime(create_time) as time1, from_unixtime(update_time) as time2 from url_extraction where domain like "%%%s%%" or url like "%%%s%%" order by create_time desc limit  $perpage offset $offset' % (domain, domain) , vars = locals())
        return form
    except Exception, e:
        return False

def select_beings_spider(offset, perpage, string = ''):
    try:
        form = db2.query('select * ,from_unixtime(create_time) as time1, from_unixtime(update_time) as time2 from tg_beings_spider where beings_id="%s" or url like "%%%s%%" order by create_time desc limit  $perpage offset $offset' % (string, string) , vars = locals())
        return form
    except Exception, e:
        return False

def select_beings(offset, perpage, string = ''):
    '''选取需抓全文的频道id'''
    try:
        if string:
            form = db.query("select * from (select 'RSS' as mode, id, beingsid as beings_id , from_unixtime(create_time) as create_time from spider.beings_extraction  union all select 'DIY',  beings_id, beings_id, from_unixtime(create_time) from taggroup.tg_beings_spider) as a  where beings_id=%s order by create_time desc limit $perpage offset $offset" % string  , vars = locals())
        else:
            form = db.query("select * from (select 'RSS' as mode,id, beingsid as beings_id , from_unixtime(create_time) as create_time from spider.beings_extraction  union all select 'DIY',beings_id, beings_id, from_unixtime(create_time) from taggroup.tg_beings_spider) as a order by create_time desc limit $perpage offset $offset"  , vars = locals())
        return form
    except Exception, e:
        return False
def del_url_extraction(id):
    return db.delete('url_extraction', where="id=$id", vars = locals())

def del_beings_spider(url_md5, beings_id):
    return db2.delete('tg_beings_spider', where="url_md5=$url_md5 and beings_id=$beings_id", vars = locals())

def update_url_extraction(id, data):
    data.update_time = int(time.time())
    a = db.update('url_extraction', update_time=data.update_time, url=data.url, name=data.name, domain=data.domain, js=data.js, mode=data.mode, info=data.info,paging=data.paging, where="id=$id", vars=locals())

def update_beings_spider(url_md5, ori_beings_id, data):
    data.update_time = int(time.time())
    a = db2.update('tg_beings_spider', update_time=data.update_time, url=data.url, content_source=data.content_source, refresh_rate=data.refresh_rate, spider_url=data.spider_url, content_start=data.content_start, beings_id=data.beings_id, url_md5=data.url_md5, where="url_md5=$url_md5 and beings_id=$ori_beings_id", vars=locals())

def select_count_url_extraction(domain = ''):
    try:
        postcount = db.query("SELECT COUNT(*) AS count FROM url_extraction where domain like '%%%s%%' or url like '%%%s%%'" % (domain, domain))[0]
        return postcount
    except Exception, e:
        return False

def select_count_beings(beings_id):
    try:
        if beings_id:
            postcount = db2.query("select sum(count) as count from (select count(*) as count from spider.beings_extraction where beingsid=%s union all select count(*) from taggroup.tg_beings_spider where beings_id= %s) as a " % (beings_id, beings_id))[0]
        else:
            postcount = db2.query("select sum(count) as count from (select count(*) as count from spider.beings_extraction  union all select count(*) from taggroup.tg_beings_spider) as a ")[0]
        return postcount
    except Exception, e:
        print e
        return False

def select_count_beings_spider(string = ''):
    try:
        postcount = db2.query("SELECT COUNT(*) AS count FROM tg_beings_spider where url like '%%%s%%' or beings_id='%s'" % (string, string))[0]
        return postcount
    except Exception, e:
        return False

def del_beings(id, mode):
    if mode == "RSS":
        return db.delete('beings_extraction', where="id=$id", vars = locals())
    elif mode == "DIY":
        return db2.delete('tg_beings_spider', where="beings_id=$id", vars = locals())

def add_beings(beings_id):
    return db.insert('beings_extraction',mode=1, js=0,charset='',paging=1, beingsid = beings_id, create_time = int(time.time()))
        
