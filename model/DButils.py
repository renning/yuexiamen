#coding: utf-8
import sys
reload(sys)
from crawlsystem.model.DB import DB
from crawlsystem.extractwork.utils import *
from config import DBCONFIG
sys.setdefaultencoding('utf-8')
def writePlaceInfo(info):
    print info
    sqlstring = "INSERT INTO yuexiamen.pre_place (name, area, areaid, placetype, address, phone, introduction, site, price, traffic, businesshours, createtime,parentplaceid, parentplacename ) VALUES (%(name)s, %(area)s, %(areaid)s, %(placetype)s, %(address)s, %(phone)s, %(introduction)s, %(site)s, %(price)s, %(traffic)s, %(businesshours)s, %(createtime)s, %(parentplaceid)s, %(parentplacename)s)"
    res = DB(**DBCONFIG).insert(sqlstring, info)
    return res


def readProInfo():
    sqlstring = "SELECT * FROM yuexiamen.pre_province"
    data = DB(**DBCONFIG).query(sqlstring)
    return data


def readAreaInfo():
    sqlstring = "SELECT * FROM yuexiamen.pre_area"
    data = DB(**DBCONFIG).query(sqlstring)
    return data


def readPlaceInfo(id):
    sqlstring = "SELECT * FROM yuexiamen.pre_place where areaid=%s order by createtime desc" % id
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
