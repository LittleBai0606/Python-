# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import time
import json
import datetime
from bs4 import BeautifulSoup
import lxml
from LianJia.items import XiaoquItem, ZaishouItem, ChengjiaoItem
from lxml import etree


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['gz.lianjia.com']
    start_urls = ['https://gz.lianjia.com/xiaoqu/']


    def start_requests(self):
            yield scrapy.Request(url= self.start_urls,callback=self.parse_daqu, dont_filter=True)

    def parse_daqu(self, response):
        dists = response.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        for dist in dists:
            url = 'https://gz.lianjia.com' + dist
            yield scrapy.Request(url=url, callback=self.parse_xiaoqu, dont_filter=True)

    def parse_xiaoqu(self, response):
        page_info = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
        page_dic = json.loads(page_info)
        page_num = page_dic.get('totalPage')
        for i in range(1,page_num + 1):
            url = response.url + 'pg' + str(i) + '/'
            yield scrapy.Request(url=url, callback=self.parse_xiaoqu_page, dont_filter=True)

    def parse_xiaoqu_page(self, response):
        xiaoqu_urls = response.xpath('//li[@class="clear xiaoquListItem"]/a/@href').extract()
        for xiaoqu_url in xiaoqu_urls:
            xiaoqu_id = xiaoqu_url.split('/')[-2]
            url = 'https://gz.lianjia.com/xiaoqu/' + xiaoqu_id + '/'
            yield scrapy.Request(url = url, callback=self.parse_xiaoqu_index, dont_filter=True)

    def parse_xiaoqu_index(self, response):
        item = LianjiaItem()
        xiaoqu = response.xpath('//h1[@class="detailTitle"]/text()').extract()[0]
        xiaoqujunjia = float(response.xpath('//span[@class="xiaoquUnitPrice"]/text()').extract()[0]) if response.xpath(
            '//span[@class="xiaoquUnitPrice"]/text()').extract() else ''
        xiaoquzuobiao = re.findall('resblockPosition:\'(.*?)\'', response.text, re.S)[0] if re.findall(
            'resblockPosition:\'(.*?)\'', response.text, re.S) else ''
        daqu = response.xpath('//div[@class="fl l-txt"]/a[3]/text()').extract()[0].rstrip('小区')
        pianqu = response.xpath('//div[@class="fl l-txt"]/a[4]/text()').extract()[0].rstrip('小区')
        soup = BeautifulSoup(response.text, 'lxml')
        xiaoquinfo = [i.text for i in soup.select('div.xiaoquInfo div')]
        xiaoqudetail = {}
        for i in xiaoquinfo:
            if key.startswith("开发商"):
                key = i[:3]
                data = i[3:]
            else:
                key = i[:4]
                data = i[4:]
            xiaoqudetail[key] = data
            xiaoqudetail['小区'] = xiaoqu
            xiaoqudetail['小区均价'] = xiaoqujunjia
            xiaoqudetail['小区坐标'] = xiaoquzuobiao
            xiaoqudetail['小区链接'] = response.url
            xiaoqudetail['大区'] = daqu
            xiaoqudetail['片区'] = pianqu
            for key in item.fields:
                if key in xiaoqudetail.keys() and (xiaoqudetail[key] != '暂无信息' and '暂无数据'):
                    item[key] = xiaoqudetail[key]
                else:
                    item[key] = ''
            yield item

            on_sale = response.xpath('//div[@class="goodSellHeader clear"]/a/@href').extract()
            if on_sale:
                yield scrapy.Request(url=on_sale[0], callback=self.parse_onsale, dont_filter=True)
            else:
                pass

            sold = response.xpath('//div[@id="frameDeal"]/a[@class="btn-large"]/@href').extract()
            if sold:
                yield scrapy.Request(url=sold[0], callback=self.parse_sold, dont_filter=True)
            else:
                pass

    def parse_onsale(self, response):
        page_info = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()
        page_dic = json.loads(page_info)
        page_num = page_dic.get('totalPage')
        on_sale_id = response.url.split('/')[-2]
        for i in range(1, page_num + 1):
            url = 'https://gz.lianjia.com/ershoufang/' + 'pg' + str(i) + on_sale_id +  '/'
            yield scrapy.Request(url=url, callback=self.parse_onsale_page, dont_filter=True)

    def parse_sold(self, response):
        page_info = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
        page_dic = json.loads(page_info)
        page_num = page_dic.get('totalPage')
        sold = response.url.split('/')[-2]
        for i in range(1, page_num + 1):
            url = 'https://gz.lianjia.com/chengjiao/' + 'pg' + str(i) + sold + '/'
            yield scrapy.Request(url=url, callback=self.parse_sold_page, dont_filter=True)

    def parse_onsale_page(self, response):
        urls = response.xpath('//ul[@class="sellListContent"]/li/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.onsale_page, dont_filter=True)

    def parse_sold_page(self, response):
        urls = response.xpath('//ul[@class="listContent"]/li/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.sold_page, dont_filter=True)

    def onsale_page(self, response):
        item = ZaishouItem()
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.select('div.title h1')[0].text
        price = float(soup.select('span.total')[0].text) if soup.select('span.total') else ''
        unitprice = float(soup.select('span.unitPriceValue')[0].text.rstrip('元/平米')) if soup.select('span.unitPriceValue') else ''
        houseID = soup.select('div.houseRecord span.info')[0].text.rstrip(' 举报') if soup.select('div.houseRecord span.info') else ''
        infos = [i.text.strip() for i in soup.select('div.introContent div.content ul li')]
        info = {}
        for i in infos:
            key = i[:4]
            data = i[4:]
            info[key] = data
            info['标题'] = title
            info['总价'] = price
            info['单价'] = unitprice
            info['链家编号'] = houseID
            info['小区'] = soup.select('div.communityName > span.label')[0].text if soup.select(
                'div.communityName > span.label') else ''
            info['房屋链接'] = response.url
            info['建筑面积'] = float(info['建筑面积'].rstrip('㎡')) if '㎡' in info['建筑面积'] else ''
            info['套内面积'] = float(info['套内面积'].rstrip('㎡')) if '㎡' in info['套内面积'] else ''
            info['挂牌时间'] = datetime.datetime.strptime(info['挂牌时间'], '%Y-%m-%d') if info['挂牌时间'] != '暂无数据' else ''
            info['关注'] = int(soup.select('span#favCount')[0].text)
            info['带看'] = int(soup.select('div.totalCount span')[0].text)
            for key in item.fields:
                if key in info.keys() and (info[key] != '暂无信息' and '暂无数据'):
                    item[key] = info[key]
                else:
                    item[key] = ''
            yield item

    def sold_page(self, response):
        item = ChengjiaoItem()
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.select('div.house-title')[0].text
        chengjiaoriqi = soup.select('div.house-title > div.wrapper > span')[0].text.split(' ')[0]
        zongjia = float(soup.select('span.dealTotalPrice > i')[0].text)
        danjia = float(soup.select('div.price > b')[0].text)
        daikan = int(soup.select('div.msg > span:nth-of-type(4) > label')[0].text)
        guanzhu = int(soup.select('div.msg > span:nth-of-type(5) > label')[0].text)
        xiaoqu = title.split(' ')[0]
        infos = [i.text.strip() for i in soup.select('div.introContent div.content ul li')]
        info = {}
        for i in infos:
            key = i[:4]
            data = i[4:]
            info[key] = data
        info['标题'] = title
        info['总价'] = zongjia
        info['单价'] = danjia
        info['成交日期'] = chengjiaoriqi
        info['小区'] = xiaoqu
        info['房屋链接'] = response.url
        info['建筑面积'] = float(info['建筑面积'].rstrip('㎡')) if '㎡' in info['建筑面积'] else ''
        info['套内面积'] = float(info['套内面积'].rstrip('㎡')) if '㎡' in info['套内面积'] else ''
        info['挂牌时间'] = datetime.datetime.strptime(info['挂牌时间'], '%Y-%m-%d') if info['挂牌时间'] != '暂无数据' else ''
        info['关注'] = guanzhu
        info['带看'] = daikan
        for key in item.fields:
            if key in info.keys() and (info[key] != '暂无数据' and '暂无信息'):
                item[key] = info[key]
            else:
                item[key] = ''
        yield item


















