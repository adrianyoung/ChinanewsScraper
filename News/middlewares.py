## -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import re
import MySQLdb
import redis
from hashlib import md5
import stem
import stem.connection
from stem import Signal
from stem.control import Controller
from scrapy import signals
from scrapy.conf import settings
from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.utils.project import get_project_settings

class RandomUserAgentMiddleware(object):
    def __init__(self, *args, **kwargs):
        self.import_settings()
        self.change_ua()

    def change_ua(self):
        db = MySQLdb.connect(self.mysql_host, self.mysql_user, self.mysql_password, self.mysql_database)
        cursor = db.cursor()
        #Highlight to change , which depends on your mysql database structure
        #A sql sentence in order to choose a random ua from mysql
        sql = "SELECT * \
               FROM UA AS t1 JOIN(\
               SELECT ROUND(RAND()*((SELECT MAX(id) FROM UA)-(SELECT MIN(id) FROM UA))+\
               (SELECT MIN(id) FROM UA)) AS id) AS t2\
               WHERE t1.id >= t2.id\
               ORDER BY t1.id LIMIT 1;"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                user_agent = row[1]
                self.settings.set('USER_AGENT', user_agent)
        except:
            print "Error:unable to fetch data"
        db.close()

    def import_settings(self):
        self.settings = get_project_settings()
        self.mysql_host        = self.settings['MYSQL_HOST']
        self.mysql_user        = self.settings['MYSQL_USER']
        self.mysql_password    = self.settings['MYSQL_PASSWORD']
        self.mysql_database    = self.settings['MYSQL_DATABASE']

    def process_request(self, request, spider):
        ua = self.settings.get('USER_AGENT')
        if ua:
            request.headers.setdefault('User-Agent', ua)

class TorProxyMiddleware(object):
    def __init__(self, *args, **kwargs):
        self.import_settings()
        self.req_counter = 0

    def change_ip_addres(self):
        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate(self.password)
            controller.signal(Signal.NEWNYM)
            controller.close()

    def import_settings(self):
        settings = get_project_settings()
        self.control_port    = settings['CONTROL_PORT']
        self.password        = settings['AUTH_PASSWORD']
        self.http_proxy      = settings['HTTP_PROXY']
        self.max_req_per_ip  = settings['MAX_REQ_PER_IP']

    def process_request(self, request, spider):
        self.req_counter += 1
        if self.max_req_per_ip is not None and self.req_counter > self.max_req_per_ip:
            self.req_counter = 0
            self.change_ip_addres()
        request.meta['proxy'] = self.http_proxy
        logging.info('Using proxy: %s' % request.meta['proxy'])
        return None

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret

class IngoreRequestMiddleware(object):
    def __init__(self, reset=False):
        self.import_settings()
        self.seeds_init()
        self.reset = reset

    def seeds_init(self):
        self.bit_size = 1 << 31
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = 'bloomfilter'
        self.blockNum = 1
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def import_settings(self):
        settings = get_project_settings()
        self.special_urls      = settings['SPECIAL_URLS']
        self.special_urls_res  = settings['SPECIAL_URLS_RES']
        self.redis_host        = settings['REDIS_HOST']
        self.redis_port        = settings['REDIS_PORT']
        self.redis_password    = settings['REDIS_PASSWORD']
        self.redis_db          = settings['REDIS_DB1']

    def isContain_redis(self, request):
        if not request.url:
            return False
        m = md5()
        m.update(request.url)
        url = m.hexdigest()
        ret = True
        name = self.key + str(int(url[0:2],16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(url)
            bit = self.r.getbit(name, loc)
            ret = ret & bool(bit)
        return ret

    def insert_redis(self, request):
        m = md5()
        m.update(request.url)
        url = m.hexdigest()
        name = self.key + str(int(url[0:2],16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(url)
            pipe = self.r.pipeline(transaction = True)
            pipe.setbit(name, loc, 1)
            pipe.execute()
        return

    @classmethod
    def from_crawler(cls, crawler):
        s = crawler.settings
        if not s.getbool('DUPLICATE_REQUEST_ENABLED'):
            raise NotConfigured
        reset = s.getbool('DUPLICATE_REQUEST_RESET')
        o = cls(reset)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def process_request(self, request, spider):
        if self.isContain_redis(request):
            if self.special_urls:
                if request.url in self.special_urls:
                    return None
            if self.special_urls_res:
                for re_pattern in self.special_urls_res:
                    if re.search(re_pattern, request.url):
                        return None
            raise IgnoreRequest("IgnoreRequest : %s" % request.url)
        else:
            self.insert_redis(request)
            return None

    def spider_opened(self, spider):
        self.pool = redis.ConnectionPool(host = self.redis_host, port = self.redis_port, password = self.redis_password, db = self.redis_db)
        self.r = redis.StrictRedis(connection_pool = self.pool)

    def spider_closed(self, spider):
        if self.reset:
            self.r.flushdb()
