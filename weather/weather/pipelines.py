# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
import json
import codecs
import pymysql
class WeatherPipeline(object):
    def process_item(self, item, spider):
        '''
        处理每一个从BeijingWeather传过来的item
        :param item:
        :param spider:
        :return:
        '''

        #获取当前工作目录
        base_dir = os.getcwd()
        #文件存在data目录下的weather.txt文件内
        filename = base_dir + '/data/weather.txt'

        #从内存以追加的方式打开文件，并写入对应的数据
        with open(filename, 'a') as f:
            f.write(item['date'] + '\n')
            f.write(item['week'] + '\n')
            f.write(item['temperature'] + '\n')
            f.write(item['weather'] + '\n')
            f.write(item['wind'] + '\n\n')

        #下载图片
        with open(base_dir + '/data/' + item['date'] + '.png', 'wb') as f:
                f.write(requests.get(item['img']).content)

        return item

class W2json(object):
    def process_item(self, item, spider):
        '''
            将爬取的信息保存到json
            方便其他程序猿调用
            :param item:
            :param spider:
            :return:
        '''

        base_dir = os.getcwd()
        filename = base_dir + '/data/weather.json'

        #打开json文件，向里面以dumps的方式写入数据
        #注意需要有一个ensure_ascii = False, 不然数据会直接为utf编码的方式存入比如"/xe15"

        with codecs.open(filename, 'a') as f:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            f.write(line)

        return item

class W2mysql(object):
    def process_item(self, item, spider):
        '''
            将爬取的信息保存到mysql
            :param item:
            :param spider:
            :return:
        '''
        date = item['date']
        week = item['week']
        temperature = item['temperature']
        weather = item['weather']
        wind = item['weather']
        img = item['img']

        #和本地的scrapyDB数据库建立连接
        connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = 'zxc958255724',
            db = 'scrapyDB',
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO WEATHER(date, week, temperature, weather, wind, img) 
                            VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (date, week, temperature, weather, wind, img))

                connection.commit()
        finally:
            connection.close()

        return item





