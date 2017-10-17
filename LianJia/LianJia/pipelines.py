# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import XiaoquItem, ZaishouItem, ChengjiaoItem

import pymongo
import pymysql

from scrapy.conf import settings

class LianjiaPipeline(object):

    collection_xiaoqu = 'collection_xiaoqu'
    collection_zaishou = 'collection_zaishou'
    collection_chengjiao = 'collection_chengjiao'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        if isinstance(item, XiaoquItem):
            self.db[self.collection_xiaoqu].update({'小区链接': item['小区链接']}, dict(item), True)
        elif isinstance(item, ZaishouItem):
            self.db[self.collection_zaishou].update({'房屋链接': item['房屋链接']}, dict(item), True)
        elif isinstance(item, ChengjiaoItem):
            self.db[self.collection_chengjiao].update({'房屋链接': item['房屋链接']}, dict(item), True)
        else:
            pass
        return item
