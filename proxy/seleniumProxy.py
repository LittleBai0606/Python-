from selenium import webdriver
import os, time

class Item(object):
    '''
    我们模拟scrapy框架
    写一个item类出来
    用来表示每一个爬到的代理
    '''
    ip= None #ip地址
    port = None
    anonymous = None
    type = None
    local = None
    speed = None

class GetProxy(object):
    '''
    获取代理的类
    '''

    def __init__(self):
        '''
        初始化整个类
        '''
        self.starturl = 'http://kuaidaili.com/free/inha/'
        self.urls = self.get_urls()
        self.proxylist = self.get_proxy_list(self.urls)
        self.filename = 'proxy.txt'
        self.saveFile(self.filename, self.proxylist)

    def get_urls(self):
        '''
        返回一个代理url的列表
        :return:
        '''
        urls = []
        for i in range(1, 2):
            url = self.starturl + str(i)
            urls.append(url)
        return urls

    def get_proxy_list(self, urls):
        '''
        返回爬取到的代理列表
        整个爬虫的关键
        :param urls:
        :return:
        '''

        browser = webdriver.PhantomJS(executable_path=r"C:\Users\BenWhite\AppData\Local\Programs\Python\Python35\Scripts\phantomjs-2.1.1-windows\bin\phantomjs.exe")
        proxy_list = []

        for url in urls:
            browser.get(url)
            browser.implicitly_wait(3)
            #找到代理table的位置
            elements = browser.find_elements_by_xpath('//tbody/tr')
            for element in elements:
                item = Item()
                item.ip = element.find_element_by_xpath('./td[1]').text
                item.port = element.find_element_by_xpath('./td[2]').text
                item.anonymous = element.find_element_by_xpath('./td[3]').text
                item.local = element.find_element_by_xpath('./td[4]').text
                item.speed = element.find_element_by_xpath('./td[5]').text
                print(item.ip)
                proxy_list.append(item)

            browser.quit()
            return proxy_list

    def saveFile(self, filename, proxy_list):
            '''
            将爬取到的结果写在本地
            :param self:
            :param filename:
            :param proxy_list:
            :return:
            '''
            base_dir = os.getcwd()
            today = time.strftime('%Y-%m-%d', time.localtime())
            fileName = base_dir + today + filename
            with open(fileName, 'w') as f:
                for item in proxy_list:

                    f.write(item.ip + '\t')
                    f.write(item.port + '\t')
                    f.write(item.anonymous + '\t')
                    f.write(item.local + '\t')
                    f.write(item.speed + '\n\n')


if __name__ == '__main__':
    Get = GetProxy()