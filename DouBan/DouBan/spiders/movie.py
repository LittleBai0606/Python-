# -*- coding: utf-8 -*-
import scrapy


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com/top250']
    start_urls = ['http://movie.douban.com/top250/']

    def parse(self, response):
        pass
