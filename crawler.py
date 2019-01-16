# -*- coding: utf-8 -*-
from utils import *
from pyquery import PyQuery
import re

class ProxyMetaclass(type):
    def __new__(cls, name,bases,attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name,bases,attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            proxies.append(proxy)
        return proxies

    def crawl_66ip(self,page_count=4):
        """
        抓取http://www.66ip.cn/网站中的代理IP
        :param page_count:抓取的总页码
        :return:代理
        """
        cookie = cookie = get_cookie_66ip()
        base_url = 'http://www.66ip.cn/{}.html'
        urls = [base_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            html = get_page(url,cookie)
            if html:
                doc = PyQuery(html)
                trs = doc('#main table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield  ':'.join([ip,port])

    def crawl_ip3366(self, page_count=4):
        base_url = 'http://www.ip3366.net/?stype=1&page={}'
        urls = [base_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            html = get_page(url)
            if html:
                doc = PyQuery(html)
                trs = doc("#list table tbody tr").items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])

    def crawl_kuaidaili(self, page_count=4):
        base_url = 'https://www.kuaidaili.com/ops/proxylist/{}/'
        urls = [base_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            html = get_page(url)
            if html:
                doc = PyQuery(html)
                trs = doc('#freelist table tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])

def crawl_xicidaili(page_count=4):
    base_url = 'https://www.xicidaili.com/nn/{}'
    urls = [base_url.format(page) for page in range(1,page_count+1)]
    for url in urls:
        html = get_page(url)
        if html:
            pattern = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>\n<td>(\d+)<td>', re.S)
            results = re.findall(pattern, html)
            for result in results:
                print(result)

        # doc = PyQuery(html)
        # trs = doc('#ip_list tbody tr:gt(0)').items()
        # # print(trs.__next__.find('td:nth-child(2)').text())
        # # print(trs.__next__)
        # for tr in trs:
        #     ip = tr.find('td:nth-child(2)').text()
        #     port = tr.find('td:nth-child(3)').text()
        #     print(ip,port)
        #     #yield ':'.join([ip, port])

    def crawl_iphai(self):
        url = 'http://www.iphai.com/'
        html = get_page(url)
        pattern = re.compile('<td>\s+(\d+.\d+.\d+.\d+)\s+</td>\s+<td>\s+(\d+)\s+</td>',re.S)
        results = re.findall(pattern, html)
        for ip, port in results:
            yield ':'.join([ip,port])

    def crawl_data5u(self):
        url = 'http://www.data5u.com/free/gngn/index.shtml'
        html = get_page(url)
        doc = PyQuery(html)
        uls = doc('body > div:nth-child(7) > ul > li:nth-child(2) > ul:gt(0)').items()
        for ul in uls:
            ip = ul.find('span:nth-child(1) > li').text()
            port = ul.find('span:nth-child(2) > li').text()
            yield ':'.join([ip,port])


# if __name__ == '__main__':
#     crawl_iphai()
