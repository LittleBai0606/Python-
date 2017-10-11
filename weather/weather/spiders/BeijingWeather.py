# -*- coding: utf-8 -*-
import scrapy

from weather.items import WeatherItem

class BeijingweatherSpider(scrapy.Spider):
    name = 'BeijingWeather'
    allowed_domains = ['tianqi.com']

    #建立需要爬取信息的url列表
    start_urls = []

    #需要爬取的城市名称，可以自行添加
    citys = ['beijing', 'guangzhou', 'hongkong']

    #用一个很简单的循环来生成需要爬的链接

    for city in citys:
        start_urls.append('http://' + city + '.tianqi.com')

    def parse(self, response):
        '''
        筛选信息的函数:
        date = 今日日期
        week = 星期几
        img = 表示天气的图片
        temperature = 当天的温度
        weather = 当天的天气
        wind = 当天的风向
        :param response:
        :return:
        '''

        #先建立一个列表，用来保存每天的信息
        items = []

        #找到包裹着每天天气信息的div
        sixday = response.xpath('//div[@class="tqshow1"]')

        #循环筛选出每天的信息:
        for day in sixday:
            # 先申请一个weatherItem 的类型来保存结果
            item = WeatherItem()

            #观察网页，知道h3标签下不单单是一行str，我们用trick的方式将它连接起来
            date = ''
            for datetitle in day.xpath('./h3//text()').extract():
                date += datetitle

            item['date'] = date
            item['week'] = day.xpath('./p//text()').extract()[0]
            item['img'] = day.xpath('./ul/li[@class="tqpng"]/img/@src').extract()[0]
            tq = day.xpath('/ul/li[2]//text()').extract()
            item['temperature'] = ''.join(tq)
            item['weather'] = day.xpath('./ul/li[3]/text()').extract()[0]
            item['wind'] = day.xpath('./ul/li[4]/text()').extract()[0]
            items.append(item)

        return items

