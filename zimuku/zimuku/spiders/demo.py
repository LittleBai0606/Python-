# -*- coding: utf-8 -*-
import scrapy

from zimuku.items import ZimukuItem

class DemoSpider(scrapy.Spider):
    #爬虫的名字
    name = 'demo'
    #规定爬虫爬取网页的域名
    allowed_domains = ['zimuku.net']
    #开始爬取的url链接
    start_urls = ['http://zimuku.net/']

    def parse(self, response):
        '''
        parse()函数接受Response参数，就是网页爬取后返回的数据
        用于处理响应，他负责解析爬取的内容
        生成解析结果的字典，并返回新的需要爬取的请求
        :param response:
        :return:
        '''

        #只爬取第一个字幕的名字
        #xpath规则可以通过查看网页源文件得出
        name = response.xpath('//b/text()').extract()[1]

        items = {}
        items['第一个'] = name

        return items


