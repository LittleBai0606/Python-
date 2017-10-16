# -*- coding: utf-8 -*-
import scrapy
from mzitu.items import MzituItem

class MeizituSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains = ['mzitu.com']
    start_urls = []

    for i in range(2, 3):
        start_urls.append('http://www.mzitu.com/page/' + str(i))

    def parse(self, response):

        #找到首页每个妹子图的li列表
        main = response.xpath('//ul[@id="pins"]/li')

        for li in main:
            #找到每个妹子图包的baseurl
            mzurl = li.xpath('./a/@href').extract()[0]
            #找到每个妹子图的名字，传回去做dirname
            name = li.xpath('.//img/@alt').extract()[0]
            #进入套图页面，抓取每一张图片
            yield scrapy.Request(mzurl, meta={'name': name, 'base_urls': mzurl}, callback =self.get_page_url)


    def get_page_url(self, response):
        '''
        找到套图的最大页码，并且生成每一页的url连接 page_url
        :param response:
        :return:
        '''

        max_num = response.xpath(
            '//div[@class="pagenavi"]/a[last()-1]/span/text()'
        ).extract()[0]
        for i in range(2, int(max_num) + 1):
            page_url = response.url + '/' + str(i)
            #这是一个生成器，用来回调img_url函数来抓套图的url链接
            yield scrapy.Request(page_url, meta={'name':response.meta['name'], 'base_urls': response.meta['base_urls']}, callback=self.get_img_url)


    def get_img_url(self, response):
        '''
        从page_url的response里
        找到图片的下载链接
        :param response:
        :return:
        '''

        item = MzituItem()
        item['name'] = response.meta['name']
        item['base_urls'] = response.meta['base_urls']

        #找到图片的下载地址
        pic = response.xpath('//div[@class="main-image"]//img/@src').extract()

        for url in pic:
            item['img_urls'] = url
            yield item
