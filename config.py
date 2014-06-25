#coding: utf-8
import pymongo
import redis
import os
import re
import logging
import logging.handlers
os.chdir(os.path.abspath(os.path.dirname(__file__)))
print os.getcwd(), os.path.abspath(os.path.dirname(__file__))

'''mysql mongo redis memorycache config'''
#mongodb and redis config
if os.path.exists('thisistest.path'):
    DBCONFIG = dict(
        DB_HOST = '192.168.1.145',
        #DB_HOST = '127.0.0.1',
        DB_PORT = 3306,
        #DB_USER = 'root',
        #DB_PWD = 'yegezi')
        DB_USER = 'writer',
        DB_PWD = 'xianguo_micblog')

    #connection = pymongo.Connection('localhost', 27017, 100)
    #db = web.database(host='211.151.83.16', dbn='mysql',
                      #db='recommend', user='reader', pw='topgene2008xianguo')
    #dblocal = web.database(host='192.168.1.145', dbn='mysql',
                           #db='recommend', user='writer', pw='xianguo_micblog')
    cache = redis.StrictRedis()
else:
    DBCONFIG = dict(
        DB_HOST = '192.168.123.31',
        DB_PORT = 3306,
        DB_USER = 'writer',
        DB_PWD = 'xianguo_micblog')
    #db = web.database(host='192.168.123.31', port=3306, dbn='mysql',
                      #db='recommend', user='writer', pw='xianguo_micblog')
    #dblocal = db
    #connection = pymongo.Connection('192.168.123.101', 27017)
    cache = redis.StrictRedis()

'''log config'''
logger = logging.getLogger()
cs = logging.StreamHandler();
logger.setLevel(logging.INFO)
rh = logging.handlers.TimedRotatingFileHandler('recommend.log', 'D')
format="[%(asctime)s](%(levelname)s)%(name)s[%(module)s]-%(funcName)s-%(lineno)d : %(message)s"
fm = logging.Formatter(format)
cs.setFormatter(fm);
rh.setFormatter(fm)
logger.addHandler(rh)
logger.addHandler(cs)


'''filter config'''
REGEXES = {
    'url': re.compile('2012\.qq\.com/twitter|list201|comment5\.news|163\.letv|index|default|/tzgc/|t\.163|v\.qq|v\.sina|slide|pic\.news|tv\.sohu|v\.ifeng|view.news|jingdian\.travel|quiz.ifeng\
        |supports\.auto|english\.sina|sms\.sina|weibo\.com|sitemap/ladyband',re.I),
    'urlpositive': re.compile('ent\.163'),
    'title': re.compile(u'调查：'),
    'unlikelyCandidatesRe': re.compile('reco|modbox|ciba_grabword_plugin|_mcePaste|contentPlayer|s-btn-jiayou|FPlayer|morepage|daodu|MASSf21674ffeef7|review-stat|nph_gallery nph_skin_white|blogzz_zzlist borderc|page-Article-QQ|pagebox|ad_text|combx|comment|community|disqus|extra|foot|header|menu|remark|rss|shoutbox|sidebar|sponsor|ad-break|agegate|pagination|pager|popup|tweet|twitter|contentPlayer|text_s1',re.I),
     'okMaybeItsACandidateRe': re.compile('voice-photoVideo|and|article|body|column|main|shadow',re.I),

    }

