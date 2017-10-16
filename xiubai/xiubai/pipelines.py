# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os, time

class XiubaiPipeline(object):
    def process_item(self, item, spider):
        base_dir = os.getcwd()
        if spider.name == 'hotspider':
            today = time.strftime('%Y-%m-%d', time.localtime())
            filename = base_dir + '/result/' + today + '_qiubai.txt'
            with open(filename, 'a+', encoding='gbk') as f:
                f.write('作者：{} \n{}\n点赞：{}\t评论数：{}\n\n'.format(
                    item['author'], item["body"], item['funNum'], item["comNum"]))

        return item
