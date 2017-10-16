# -*- coding: utf-8 -*-
import scrapy

from xiubai.items import XiubaiItem

class HotspiderSpider(scrapy.Spider):
    name = 'hotspider'
    allowed_domains = ['qiushibaike.com']
    start_urls = []

    for i in range(1, 6):
        start_urls.append('https://www.qiushibaike.com/8hr/page/' + str(i) + '/')

    def parse(self, response):
        items = []

        main = response.xpath('//div[@id="content-left"]/div')

        for div in main:
            item = XiubaiItem()
            # 段子作者
            item['author'] = div.xpath('.//h2/text()').extract()[0]
            # 段子主体：
            item['body'] = ''.join(div.xpath('a[@class="contentHerf"]/div/span[1]/text()').extract())
            # 段子footer
            item['funNum'] = div.xpath('.//span[@class="stats-vote"]/i/text()').extract()[0]
            item['comNum'] = div.xpath('.//span[@class="stats-comments"]/a/i/text()').extract()[0]
            items.append(item)

        return items

