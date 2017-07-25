# -*- coding: utf-8 -*-
import config
import db
import requests
import re
from multiprocessing import Pool

mon = db.dlmongodb()
mon.initdb()
p = 0


def getHtml(url):
    try:
        r = requests.get(url=url, headers=config.get_header(), timeout=config.TIMEOUT)

        if (not r.ok) or (r.content) < 500:
            print '提取淘宝商品失败'
        else:
            print '提取淘宝商品成功'
            return r.text
    except Exception:
        print Exception.message


def delhtml(html, goods):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)

        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            mon.db.taobao2.insert(dict(title=title, price=price))

    except Exception:
        print('处理网页错误')


def main(goods):
    global p
    start_url = 'https://s.taobao.com/search?q=' + goods
    sopage = 2
    for i in range(sopage):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = getHtml(url)
            delhtml(html, goods)
        except:
            continue
    p = p + 1
    print 'item : ' + str(p) + ' finished'


if __name__ == '__main__':
    pool = Pool()
    groups = ([u['url'] for u in mon.db.source.find()])
    pool.map(main,groups)
    pool.close()
    pool.join()

