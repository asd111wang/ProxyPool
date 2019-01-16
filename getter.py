# -*- coding: utf-8 -*-
import sys
from db import RedisClient
from crawler import Crawler
import time

class Getter():
    def __init__(self):
        self.crawler = Crawler()
        self.db = RedisClient()

    def run(self):
        print('获取器开始执行')
        for callback_label in range(self.crawler.__CrawlFuncCount__):
            callback = self.crawler.__CrawlFunc__[callback_label]
            #print(callback)
            proxies = self.crawler.get_proxies(callback)
            sys.stdout.flush()
            #print(len(proxies))
            for proxy in proxies:
                #print(proxy)
                if not self.db.add(proxy):
                    print('添加失败',proxy,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

if __name__ == '__main__':
     Getter().run()
