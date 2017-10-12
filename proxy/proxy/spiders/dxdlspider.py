# -*- coding: utf-8 -*-
import scrapy

from proxy.items import ProxyItem

class DxdlspiderSpider(scrapy.Spider):
    name = 'dxdlspider'
    allowed_domains = ['xicidaili.com']
    start_urls = []

    for i in range(1, 6):
        start_urls.append('http://www.xicidaili.com/nn/' +str(i))

    def parse(self, response):
        subSelector = response.xpath('//tr[@class=""]|//tr[@class="odd"]')
        items = []
        for sub in subSelector:
            item = ProxyItem()
            ip= sub.xpath('.//td[2]/text()').extract()[0]
            port= sub.xpath('.//td[3]/text()').extract()[0]
            item['addr'] = ip + ':' + port;
            items.append(item)
        return items



