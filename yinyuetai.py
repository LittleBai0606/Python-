import os
import requests
import bs4
import random

def get_html(url):

    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'Something wrong!'

def get_agent():
    '''
    模拟header的user-agent字段，
    返回一个随机的user-agent字典类型的键值对
    :return:
    '''

    agents = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
              'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)']
    fakeheader = {}
    fakeheader['User-agent'] = agents[random.randint(0, len(agents))]
    return fakeheader

def get_proxy():
    '''
    简单模拟代理池
    返回一个字典类型的键值对
    :return:
    '''

    proxy = ["http://203.91.121.76:3128",
             "http://123.7.38.31:9999",
             "http://218.56.132.155:8080",
             "http://220.249.185.178:9999",
             "http://218.66.253.145:8800",
             "http://110.73.15.81:80",
             "http://61.163.39.70:9999",
             "http://27.44.174.134:9999"]
    fakepxs = {}
    fakepxs['http'] = proxy[random.randint(0, len(proxy))]
    return fakepxs

def get_content(url):
    #我们来打印一下表头
    if url[-2:] == 'ML':
        print('内地排行榜')
    elif url[-2:] == 'HT':
        print('港台排行榜')
    elif url[-2:] == 'US':
        print('欧美排行榜')
    elif url[-2:] == 'KR':
        print('韩国排行榜')
    else:
        print('日本排行榜')

    #找到我们需要的每一个标签
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    li_list = soup.find_all('li', attrs={'name' : 'dmvLi'})

    for li in li_list:
        match = {}
        try:
            # 判断分数的升降！
            if li.find('h3', class_='desc_score'):
                match['分数'] = li.find('h3', class_='desc_score').text
            else:
                match['分数'] = li.find('h3', class_='asc_score').text

            match['排名'] = li.find('div', class_='top_num').text
            match['名字'] = li.find('a', class_='mvname').text
            match['发布时间'] = li.find('p', class_='c9').text
            match['歌手'] = li.find('a', class_='special').text

        except:
            return ""
        print(match)


def main():
    base_url = "http://vchart.yinyuetai.com/vchart/trends?area="
    suffix = ['ML','HT','US','JP','KR']
    for suff in suffix:
        url = base_url+suff
        print()
        get_content(url)


if __name__ == '__main__':
    main()