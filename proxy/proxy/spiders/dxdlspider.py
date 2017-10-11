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
        #先实例化一个item
        item = ProxyItem()

        main = response.xpath('//table[@id=ip_list]/tbody/tr')

        for li in main:
            ip = li.xpath('td/text()').extract()[1]
            port = li.xpath('td/text()').extract()[2]
            item['addr'] = ip + ':' + port
            yield item



