# -*- coding: utf-8 -*-
import scrapy
from ..items import BookItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['book.douban.com']
    start_urls = 'https://book.douban.com/top250'

    

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse_book_list, dont_filter=True)

    def parse_book_list(self, response):
        for i in range(10):
            current_url = response.url + '?start=' + str(i * 25)
            yield scrapy.Request(url=current_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        selector = scrapy.Selector(response)
        infos = selector.xpath('//tr[@class="item"]')
        item = BookItem()
        for info in infos:
            item['name'] = info.xpath('./td/div/a/@title').extract()[0]
            item['url'] = info.xpath('./td/div/a/@href').extract()[0]
            author_info = info.xpath('./td/p/text()').extract()[0]
            author_infos = author_info.split('/')
            item['price'] = str(author_infos[len(author_infos) -1])
            item['author'] = author_infos[0]
            item['pubday'] = author_infos[len(author_infos) - 2]
            item['rating_nums'] = info.xpath('./td/div/span[2]/text()').extract()[0]
            comment_nums = info.xpath('normalize-space(td/div/span[3]/text())').extract()[0]
            item['comment_nums'] = comment_nums.replace('( ', '').replace('人评价 )', '')
            quote = info.xpath('td/p/span[@class="inq"]/text()').extract()
            if len(quote) > 0:
                quote = quote[0]
            else:
                quote = ''
            item['quote'] = quote
            yield item


















