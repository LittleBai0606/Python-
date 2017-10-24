# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ..items import MovieItem

#<span class="other">&nbsp;/&nbsp;月黑高飞(港)  /  刺激1995(台)</span>
#//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[1]
class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start_urls = 'https://movie.douban.com/top250'

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse_movie_list, dont_filter=True)

    def parse_movie_list(self, response):
        for i in range(10):
            current_url = response.url + '?start=' + str(i * 25)
            yield scrapy.Request(url=current_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        selector = scrapy.Selector(response)
        infos = selector.xpath('//ol[@class="grid_view"]/li')
        item = MovieItem()
        for info in infos:
            item['name'] = info.xpath('.//div[@class="hd"]/a/span[1]/text()').extract()[0]
            othername= info.xpath('.//span[@class="other"]/text()').extract()
            item['othername'] = othername[0].replace('\xa0', '').replace('  ', '')
            description = info.xpath('.//div[@class="bd"]/p[1]/text()').extract()
            list = description[0].replace('\xa0\xa0\xa0', '\t').replace('\r\n', '').replace(' ', '').replace('\n', '').split('\t')
            director = list[0].split(':')
            item['director'] = director[1]
            item['time'] = description[1].replace('\xa0', '').replace('\r\n', '').replace('\n', '').replace('  ', '').split('/')[0]
            item['country'] = description[1].replace('\xa0', '').replace('\r\n', '').replace('\n', '').replace('  ', '').split('/')[1]
            item['type'] = description[1].replace('\xa0', '').replace('\r\n', '').replace('\n', '').replace('  ', '').split('/')[2]
            item['rating_nums'] = info.xpath('.//span[@class="rating_num"]/text()').extract()[0]
            item['comment_nums'] = info.xpath('.//div[@class="star"]/span[4]/text()').extract()[0].replace('人评价', '')
            item['url'] = info.xpath('.//div[@class="pic"]/a/@href').extract()[0]
            quote = info.xpath('.//span[@class="inq"]/text()').extract()
            if len(quote) > 0:
                quote = quote[0]
            else:
                quote = ''
            item['quote'] = quote
            yield item




