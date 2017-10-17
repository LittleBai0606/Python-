# -*- coding: utf-8 -*-
import scrapy
from ..items import JiandanItem

#//*[@id="comment-3588994"]/div/div/div[2]/p/img
class MeiziSpider(scrapy.Spider):
    name = 'meizi'
    allowed_domains = ['jandan.net']
    start_urls = 'http://jandan.net/ooxx'

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        current_page = response.xpath('//span[@class="current-comment-page"]/text()').extract()[0]
        current_page = current_page.replace('[', '').replace(']', '')
        for i in range(1, int(current_page)+1):
            page_url = 'http://jandan.net/ooxx/page-' + str(i) + '#comments'
            yield scrapy.Request(url=page_url, callback=self.parse_meiziPic, dont_filter=True)

    def parse_meiziPic(self, response):
        lists = response.xpath('//ol[@class="commentlist"]/li')
        for list in lists:
            item = JiandanItem()
            picUrl = response.xpath('.//p/img/@src').extract()[0]
            if picUrl.endswith('.gif'):
                break
            item['author'] = response.xpath('.//div[@class="author"]/strong/text()').extract()[0]
            item['picUrl'] = 'https:' + picUrl
            yield item







