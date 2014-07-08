#coding: utf-8
import json
import tornado.web
import tornado.escape
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
import tornado.gen
from yuexiamen.model import DButils
import time
import config
import hashlib
logger = config.logger
cache = config.cache
class MudidiHandler(tornado.web.RequestHandler):
    def get(self):
        proitems = DButils.readProInfo()
        print proitems
        areaitems = DButils.readAreaInfo()
        areas = dict()
        for item in areaitems:
            areas.setdefault(item['provinceid'], [])
            areas[item['provinceid']].append(item)
        return self.render('sidebar.html', items=proitems, areas=areas )


class PlaceAddHandler(tornado.web.RequestHandler):
    def get(self, id, name):
        print id, name
        return self.render('addplace.html', id=id, name=name)

    def post(self,areaid, area):
        print self.request.files
        file_dict_list = self.request.files['img']

        for file_dict in file_dict_list:
            filename = file_dict["filename"]
            f = open("imgfile/upload/%s" % areaid, "wb")
            f.write(file_dict["body"])
            f.close()
        name = self.get_argument('placename')
        placetype = self.get_argument('type', )
        address = self.get_argument('address')
        phone = self.get_argument('phone', 0)
        introduction = self.get_argument('introduction')
        site = self.get_argument('site')
        price = self.get_argument('price')
        traffic = self.get_argument('traffic')
        businesshours = self.get_argument('businesshours')
        info = dict(name=name,
                    area=area,
                    areaid=areaid,
                    placetype=placetype,
                    address=address,
                    phone=phone,
                    introduction=introduction,
                    site=site,
                    price=price,
                    traffic=traffic,
                    createtime=time.time(),
                    parentplaceid = None,
                    parentplacename = None,
                    businesshours=businesshours)

        DButils.writePlaceInfo(info)
        items = DButils.readPlaceInfo(areaid)
        self.render('place.html', items=items, id=areaid, name=area)


class PoiAddHandler(tornado.web.RequestHandler):
    def get(self, id, name):
        print id, name
        return self.render('addpoi.html', id=id, name=name)

    def post(self,areaid, area):
        #print self.request.files
        #file_dict_list = self.request.files['img']

        #for file_dict in file_dict_list:
            #filename = file_dict["filename"]
            #f = open("imgfile/upload/%s" % areaid, "wb")
            #f.write(file_dict["body"])
            #f.close()
        name = self.get_argument('placename')
        introduction = self.get_argument('introduction')
        info = dict(name=name,
                    area=area,
                    areaid=areaid,
                    introduction=introduction,
                    createtime=time.time(),
                    )
        DButils.writePoiInfo(info)
        items = DButils.readPoiInfo(areaid)
        self.render('poi.html', items=items, id=areaid, name=area,)


class ChildPlaceAddHandler(tornado.web.RequestHandler):
    def get(self, id1,name1,  id2, name2):
        return self.render('addplace.html', id1=id1, id2=id2, name=name2)

    def post(self,areaid, area, id2, name2):
        name = self.get_argument('placename')
        placetype = self.get_argument('type', )
        address = self.get_argument('address')
        phone = self.get_argument('phone', 0)
        introduction = self.get_argument('introduction')
        site = self.get_argument('site')
        price = self.get_argument('price')
        traffic = self.get_argument('traffic')
        businesshours = self.get_argument('businesshours')
        #parentplaceid = self.get_argument('parentplaceid', None)
        #parentplacename = self.get_argument('parentplacename', None)
        info = dict(name=name,
                    area=area,
                    areaid=areaid,
                    placetype=placetype,
                    address=address,
                    phone=phone,
                    introduction=introduction,
                    site=site,
                    price=price,
                    traffic=traffic,
                    createtime=time.time(),
                    parentplaceid = id2,
                    parentplacename = name2,
                    businesshours=businesshours)

        DButils.writePlaceInfo(info)
        items = DButils.readPlaceInfo(areaid)
        self.render('place.html', items=items, id=areaid, name=area, )


class PoiadminHandler(tornado.web.RequestHandler):
    def get(self, id, name):
        items = DButils.readPoiInfo(id)
        return self.render('poiadmin.html', items=items, id=id, name=name)


class PoiHandler(tornado.web.RequestHandler):
    def get(self, id, name):
        items = DButils.readPoiInfo(id)
        return self.render('poi.html', items=items, id=id, name=name)


class PlaceHandler(tornado.web.RequestHandler):
    def get(self, id, name):
        items = DButils.readPlaceInfo(id)
        return self.render('place.html', items=items, id=id, name=name)
