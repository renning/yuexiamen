#coding: utf-8
from crawlsystem.model.DB import DB
from crawlsystem.extractwork.utils import *
from config import DBCONFIG
def writeRuleInfo(info):
    sqlstring = "INSERT INTO crawlsystem.crawl_url_extract_info (domain, name, url_example, url_regular, crawl_info) VALUES (%(domain)s,%(name)s,%(url_example)s, %(url_regular)s, %(crawl_info)s)"
    res = DB(**DBCONFIG).insert(sqlstring, info)
    return res


def writeRssInfo(info):
    sqlstring = "INSERT INTO crawlsystem.crawl_rss_extract_info (name, url, crawl_info) VALUES (%(name)s,%(url)s,  %(crawl_info)s)"
    res = DB(**DBCONFIG).insert(sqlstring, info)
    return res


def readRssInfo(string):
    if string:
        sqlstring = "SELECT * FROM crawlsystem.crawl_rss_extract_info WHERE CONCAT（name, url） LIKE '%%%s%%'" % string
    else:
        sqlstring = "SELECT * FROM crawlsystem.crawl_rss_extract_info"
    data = DB(**DBCONFIG).query(sqlstring)
    return data


def getCrawlInfo(url):
    domain = getDomain(url)
    sqlstring = 'select * from crawlsystem.crawl_url_extract_info where domain = "%s"' % domain
    data = DB(**DBCONFIG).query(sqlstring)
    extractinfos = []
    for dt in data:
        if re.compile(dt['urlregular']).search(self.url):
            extractinfos.append(dt['extractinfo'])
    return extractinfos

#getCrawlInfo(u'http://www.google.com')
