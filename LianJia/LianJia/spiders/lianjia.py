# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import time
from LianJia.items import LianjiaItem
from lxml import etree
from scrapy_redis.spiders import RedisSpider


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['gz.lianjia.com']
    start_urls = []
    regions = {
        'tianhe' : '天河',
        'yuexiu' : '越秀',
        'liwan' : '荔湾',
        'haizhu' : '海珠',
        'panyu' : '番禺',
        'baiyun' : '白云',
        'huangpugz' : '黄埔',
        'conghua' : '从化',
        'zengcheng' : '增城',
        'huadou' : '花都',
        'nansha' : '南沙'
    }

    for region in list(regions.keys()):
        start_urls.append("https://gz.lianjia.com/chengjiao/" + region + "/")


    def parse(self, response):
        pass
