import requests
import os
from bs4 import BeautifulSoup

def get_html(url):

    r = requests.get(url, timeout = 30)
    r.raise_for_status()
    r.encoding = 'gbk'
    return r.text

def get_content(url):

    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    #找到电影排行榜的ul列表
    movie_list = soup.find('ul', class_ = 'picList clearfix')
    movies = movie_list.find_all('li')

    for top in movies:
        img_url = 'http:' + top.find('img')['src']
        print(img_url)
        name = top.find('span', class_ = 'sTit').a.text
        try:
            time = top.find('span', class_ = 'sIntro').text
        except:
            time = '暂无上映时间'

        actors = top.find('p', class_ = 'pActor')
        actor = ''
        for act in actors.contents:
            actor = actor + act.string + '  '

        #找到影片简介
        intro = top.find('p', class_ = 'pTxt pIntroShow').text
        print("片名：{}\t{}\n{}\n{} \n \n ".format(name, time, actor, intro))

        with open("D:/img/" + name + ".png", 'wb+' ) as f:
            f.write(requests.get(img_url).content)

def main():
    url = 'http://dianying.2345.com/top/'
    get_content(url)

if __name__ == '__main__':
    main()