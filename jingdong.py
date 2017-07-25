# -*- coding: utf-8 -*-
import config
import db
import requests
from bs4 import  BeautifulSoup
import  re
import  chardet
mon = db.dlmongodb()
mon.initdb()
def getHtml(url):
    try:
        r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT)
        r.encoding ='utf-8'
        if(not r.ok)or (r.content)<500:
            print '提取京东商品失败'
        else:
            print '提取京东商品成功'
            return r.text
    except Exception:
        print Exception.message


def delhtml(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        lis = soup.find_all(class_='gl-item')
        for i in range(len(lis)):
            title=lis[i].find(class_="p-name").text.strip()
            price=lis[i].find(class_="p-price").text.strip()[1:]
            mon.db.jingdong.insert(dict(title=title,price=price))

    except Exception:
        print('处理网页错误')




def main():
    p=1
    for u in mon.db.source.find():
        goods=u['url']
        start_url='https://search.jd.com/Search?enc=utf-8&keyword='+goods
        sopage=2
        for i in range(sopage):
            try:
                url=start_url+'&page='+str(i*2-1)
                html=getHtml(url)
                delhtml(html)
            except:
                continue

        print 'item : '+str(p)+' finished'
        p=p+1

main()
