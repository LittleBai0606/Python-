# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os, requests
import urllib

class MzituPipeline(object):


    def process_item(self, item, spider):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
            'Referer': item['base_urls'],

        }
        base_dir = 'D:/meizitu/'
        # 防止目录不存在！
        if not os.path.exists(base_dir + item['name']):
            os.makedirs(base_dir + item['name'])

        # 生成图片下载列表：
        open(base_dir + item['name'] + '/' + item['img_urls'][-6:], 'wb').write(requests.get(item['img_urls'], headers = headers).content)
        return item

