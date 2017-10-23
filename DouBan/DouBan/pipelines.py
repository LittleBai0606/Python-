# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class W2mysql(object):
    def process_item(self, item, spider):
        '''
            将爬取的信息保存到mysql
            :param item:
            :param spider:
            :return:
        '''
        name = item['name']
        author = item['author']
        rating_nums = item['rating_nums']
        comment_nums = item['comment_nums']
        quote = item['quote']
        pubday = item['pubday']
        price = item['price']
        url = item['url']

        #和本地的scrapyDB数据库建立连接
        connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = 'zxc958255724',
            db = 'doubanspider',
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO BOOK(name, author, pubday, price, rating_nums, comment_nums, quote, url) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (name, author, pubday, price, rating_nums, comment_nums, quote, url))

                connection.commit()
        finally:
            connection.close()

        return item