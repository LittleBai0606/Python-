# -*- coding: utf-8 -*-
import scrapy

from proxy.items import ProxyItem

class KdlspiderSpider(scrapy.Spider):
    name = 'kdlspider'
    allowed_domains = ['kuaidaili.com']
    start_urls = []

    for i in range(1, 6):
        start_urls.append('http://www.kuaidaili.com/free/inha/' + str(i) + '/')

    def parse(self, response):
        #先实例化一个item
        items = []

        main = response.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')

        for li in main:
            item = ProxyItem()
            item['ip'] = li.xpath('td/text()').extract()[0]
            item['port'] = li.xpath('td/text()').extract()[1]
            item['protocol'] = li.xpath('td/text()').extract()[2]
            item['type'] = li.xpath('td/text()').extract()[3]
            item['location'] = li.xpath('td/text()').extract()[4]
            item['source'] = 'kuaidaili'
            items.append(item)
        return items

