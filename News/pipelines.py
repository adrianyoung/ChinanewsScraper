# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import datetime
import json
from scrapy.exceptions import DropItem
import redis
from hashlib import md5
from scrapy.conf import settings
from scrapy.utils.project import get_project_settings
class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed
    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret

class RedisDuplicatePipeline(object):
    def __init__(self):
        self.import_settings()
        self.seeds_init()

    def seeds_init():
        self.bit_size = 1 << 31
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = 'bloomfilter'
        self.blockNum = 1
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def import_settings(self):
        self.settings = get_project_settings()
        self.reset             = self.settings['DUPLICATE_ITEM_RESET']
        self.redis_host        = self.settings['REDIS_HOST']
        self.redis_port        = self.settings['REDIS_PORT']
        self.redis_password    = self.settings['REDIS_PASSWORD']
        self.redis_db          = self.settings['REDIS_DB2']

    def isContain_redis(self, item):
        if not item:
            return False
        m = md5()
        m.update(str(item))
        item = m.hexdigest()
        ret = True
        name = self.key + str(int(item[0:2],16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(item)
            bit = self.r.getbit(name, loc)
            ret = ret & bool(bit)
        return ret

    def insert_redis(self, item):
        m = md5()
        m.update(str(item))
        item = m.hexdigest()
        name = self.key + str(int(item[0:2],16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(item)
            pipe = self.r.pipeline(transaction = True)
            pipe.setbit(name, loc, 1)
            pipe.execute()
        return

    def process_item(self, item, spider):
        if self.isContain_redis(item):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.insert_redis(item)
            return item

    def open_spider(self, spider):
        self.pool = redis.ConnectionPool(host = redis_host, port = redis_port, password = redis_password, db = redis_db)
        self.r = redis.StrictRedis(connection_pool = self.pool)

    def close_spider(self, spider):
        if self.reset:
            self.r.flushdb()


class MongodbPipeline(object):
    def __init__(self):
        self.import_settings()

    def import_settings(self):
        self.settings = get_project_settings()
        self.mongo_uri   = self.settings['MONGO_URI']
        self.mongo_db    = self.settings['MONGO_DATABASE']

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        db = self.db

        if item['news_type'] == 'cul':

            collection = db.wh

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'mil':

            collection = db.mil

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'gj':

            collection = db.gj

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'yl':

            collection = db.yl

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'jk':

            collection = db.jk

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'ty':

            collection = db.ty

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'sh':

            collection = db.sh

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'hr':

            collection = db.hr

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'fortune':

            collection = db.fortune

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'cj':

            collection = db.cj

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'it':

            collection = db.it

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'ny':

            collection = db.ny

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'ga':

            collection = db.ga

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'house':

            collection = db.estate

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'auto':

            collection = db.auto

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        elif item['news_type'] == 'tw':

            collection = db.tw

            item['submission_date'] = datetime.datetime.utcnow()
            collection.insert_one(item)

        return item
