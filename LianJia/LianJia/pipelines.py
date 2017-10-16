# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Lianjia.items import XiaoquItem, ZaishouItem, ChengjiaoItem

import pymongo

class LianjiaPipeline(object):


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


