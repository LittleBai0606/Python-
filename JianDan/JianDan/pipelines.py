# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os,time
import requests


class JiandanPipeline(object):
    def process_item(self, item, spider):
        base_dir = 'D:/jiandan/'
        headers = {'referer': 'http://jandan.net/',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        # 防止目录不存在！
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # 生成图片下载列表：
        open(base_dir + time.strftime("%H%M%S") + '.jpg', 'wb').write(
            requests.get(item['picUrl'],headers = headers).content)
        return item

