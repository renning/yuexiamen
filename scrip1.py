#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
s = '''http://www.mafengwo.cn/mdd/smap.php?mddid=10115">安徽
http://www.mafengwo.cn/mdd/smap.php?mddid=10844">澳门
http://www.mafengwo.cn/mdd/smap.php?mddid=10848">北京市
http://www.mafengwo.cn/mdd/smap.php?mddid=10153">福建
http://www.mafengwo.cn/mdd/smap.php?mddid=10227">甘肃
http://www.mafengwo.cn/mdd/smap.php?mddid=10383">广东
http://www.mafengwo.cn/mdd/smap.php?mddid=10112">广西
http://www.mafengwo.cn/mdd/smap.php?mddid=10104">贵州
http://www.mafengwo.cn/mdd/smap.php?mddid=10325">海南
http://www.mafengwo.cn/mdd/smap.php?mddid=10225">河北
http://www.mafengwo.cn/mdd/smap.php?mddid=10114">河南
http://www.mafengwo.cn/mdd/smap.php?mddid=10262">黑龙江
http://www.mafengwo.cn/mdd/smap.php?mddid=10224">湖北
http://www.mafengwo.cn/mdd/smap.php?mddid=10123">湖南
http://www.mafengwo.cn/mdd/smap.php?mddid=10324">吉林
http://www.mafengwo.cn/mdd/smap.php?mddid=10100">江苏
http://www.mafengwo.cn/mdd/smap.php?mddid=10263">江西
http://www.mafengwo.cn/mdd/smap.php?mddid=10226">辽宁
http://www.mafengwo.cn/mdd/smap.php?mddid=10066">内蒙古
http://www.mafengwo.cn/mdd/smap.php?mddid=10441">宁夏
http://www.mafengwo.cn/mdd/smap.php?mddid=10110">青海
http://www.mafengwo.cn/mdd/smap.php?mddid=10098">山东
http://www.mafengwo.cn/mdd/smap.php?mddid=10109">山西
http://www.mafengwo.cn/mdd/smap.php?mddid=10384">陕西
http://www.mafengwo.cn/mdd/smap.php?mddid=10849">上海市
http://www.mafengwo.cn/mdd/smap.php?mddid=10107">四川
http://www.mafengwo.cn/mdd/smap.php?mddid=10074">台湾
http://www.mafengwo.cn/mdd/smap.php?mddid=10847">天津市
http://www.mafengwo.cn/mdd/smap.php?mddid=10025">西藏
http://www.mafengwo.cn/mdd/smap.php?mddid=10845">香港
http://www.mafengwo.cn/mdd/smap.php?mddid=10081">新疆
http://www.mafengwo.cn/mdd/smap.php?mddid=10028">云南
http://www.mafengwo.cn/mdd/smap.php?mddid=10111">浙江
http://www.mafengwo.cn/mdd/smap.php?mddid=10846">重庆市'''
s = s.split('\n')
s = [dict(name=i.split('">')[1], mfwid=i.split('">')[0][-5:], countryid=1) for i in s]
from crawlsystem.model.DB import DB
from config import DBCONFIG

'''ru ku sheng
from crawlsystem.model.DB import DB
from config import DBCONFIG

for info in s:
    print info
    sqlstring = "INSERT INTO yuexiamen.pre_province (countryid, name, mfwid) VALUES (%(countryid)s,%(name)s, %(mfwid)s)"
    res = DB(**DBCONFIG).insert(sqlstring, info)'''

import urllib2, re, time
sqlstring = "SELECT * FROM yuexiamen.pre_province"
data = DB(**DBCONFIG).query(sqlstring)
print data

for i in data:
    mfwid = i['mfwid']
    url = 'http://www.mafengwo.cn/jd/%s/gonglve.html' % mfwid
    print url

    #url = 'http://www.mafengwo.cn/jd/12711/gonglve.html'
    file = urllib2.urlopen(url).read().decode('utf-8')
    kk = re.compile(u'全部</a>([\s\S]*?)</dd>').findall(file)
    print kk
    if kk:
        kk = kk[0]
        kk = re.compile(u'<a href="/jd/(.*?)/gonglve.html" target="_blank"><h2>(.*?)</h2').findall(kk)
        for id, name in kk:
            ss = dict(provinceid=mfwid, countryid=1, name=name, mfwid=id)
            print id, name
            sqlstring = "INSERT INTO yuexiamen.pre_area (countryid, name, mfwid, provinceid) VALUES (%(countryid)s,%(name)s, %(mfwid)s, %(provinceid)s)"
            res = DB(**DBCONFIG).insert(sqlstring,ss)
    time.sleep(2)
