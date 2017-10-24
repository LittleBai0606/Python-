# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    rating_nums = scrapy.Field()#评分
    quote = scrapy.Field()#一句话介绍，推荐
    comment_nums = scrapy.Field()#评价人数
    pubday = scrapy.Field()#出版日期
    price = scrapy.Field()
    url = scrapy.Field()

class MovieItem(scrapy.Item):
    name = scrapy.Field()
    othername = scrapy.Field()
    rating_nums = scrapy.Field()
    quote = scrapy.Field()
    comment_nums = scrapy.Field()
    director = scrapy.Field()
    time = scrapy.Field()
    country = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()



