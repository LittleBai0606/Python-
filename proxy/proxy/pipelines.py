# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

class ProxyPipeline(object):
    def process_item(self, item, spider):

        base_dir = os.getcwd()
        if spider.name == 'dxdlspider':
            fiename = base_dir + '/result/dxdl_proxy.txt'
            open(fiename, 'a').write(item['addr'] + '\n')

        elif spider.name == 'kdlspider':
            fiename = base_dir + '/result/kdl_proxy.txt'
            open(fiename, 'a').write(item['addr'] + '\n')

        return item
