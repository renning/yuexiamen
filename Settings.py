import os
DEBUG = True
DIRNAME = os.path.dirname(__file__)
STATIC_PATH = os.path.join(DIRNAME, 'static')
TEMPLATE_PATH = os.path.join(DIRNAME, 'template')

import logging
logger = logging.getLogger()
cs = logging.StreamHandler();
logger.setLevel(logging.INFO)
rh = logging.handlers.TimedRotatingFileHandler('server.log', 'D')
format="[%(asctime)s](%(levelname)s)%(name)s[%(module)s]-%(funcName)s-%(lineno)d : %(message)s"
fm = logging.Formatter(format)
cs.setFormatter(fm);
rh.setFormatter(fm)
logger.addHandler(rh)
logger.addHandler(cs)

if os.path.exists('thisistest.path'):
    DBCONFIG = dict(
        DB_HOST = '192.168.1.145',
        DB_PORT = 3306,
        DB_USER = 'writer',
        DB_PWD = 'xianguo_micblog')
else:
    DBCONFIG = dict(
        DB_HOST = '192.168.123.31',
        DB_PORT = 3306,
        DB_USER = 'writer',
        DB_PWD = 'xianguo_micblog')

#import base64
#import uuid
#base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
COOKIE_SECRET = 'L8LwECiNRxq2N0N2eGxx9MZlrpmuMEimlydNX/vt1LM='
