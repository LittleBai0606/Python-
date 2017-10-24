# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from .items import BookItem, MovieItem

class W2mysql(object):
    def process_item(self, item, spider):
        if isinstance(item, BookItem):
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

        if isinstance(item, MovieItem):
            movie_name = item['name']
            movie_othername = item['othername']
            movie_rating_nums = item['rating_nums']
            movie_quote = item['quote']
            movie_comment_nums = item['comment_nums']
            movie_director = item['director']
            movie_time = item['time']
            movie_country = item['country']
            movie_type = item['type']
            movie_url = item['url']

            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='zxc958255724',
                db='doubanspider',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

            try:
                with connection.cursor() as cursor:
                    moive_sql = """INSERT INTO movie(movie_name, movie_othername, movie_director, movie_time, movie_country, movie_type, movie_quote, movie_rating_nums, movie_comment_nums, movie_url) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(moive_sql, (movie_name, movie_othername, movie_director, movie_time, movie_country, movie_type, movie_quote, movie_rating_nums, movie_comment_nums, movie_url))

                    connection.commit()
            finally:
                connection.close()

            return item
