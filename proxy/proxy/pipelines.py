# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import time

class ProxyPipeline(object):
    def process_item(self, item, spider):

        base_dir = os.getcwd()
        if spider.name == 'dxdlspider':
            today = time.strftime('%Y-%m-%d', time.localtime())
            filename = base_dir + '/result/' + today + '_dxdl_proxy.txt'
            with open(filename, 'a') as fp:
                fp.write(item['ip'].strip() + '\t')
                fp.write(item['port'].strip() + '\t')
                fp.write(item['protocol'].strip() + '\t')
                fp.write(item['type'].strip() + '\t')
                fp.write(item['location'].strip() + '\t')
                fp.write(item['source'].strip() + '\t\n')

        elif spider.name == 'kdlspider':
            today = time.strftime('%Y-%m-%d', time.localtime())
            filename = base_dir + '/result/' + today + '_kdl_proxy.txt'
            with open(filename, 'a') as fp:
                fp.write(item['ip'].strip() + '\t')
                fp.write(item['port'].strip() + '\t')
                fp.write(item['protocol'].strip() + '\t')
                fp.write(item['type'].strip() + '\t')
                fp.write(item['location'].strip() + '\t')
                fp.write(item['source'].strip() + '\t\n')

        return item
