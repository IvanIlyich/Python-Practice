# -*- coding: utf-8 -*-
import scrapy
import bs4
import sys
import csv
import urllib

from X.items import SingerItem

reload(sys)
sys.setdefaultencoding('utf8')


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["wikipedia.org"]
    lines = []
    with open("musicians_out_I.csv", 'rb') as csvfile:
        reader = csv.reader(csvfile)
        lines.extend([line for line in reader][1:])
    with open("musicians_out_II.csv", 'rb') as csvfile:
        reader = csv.reader(csvfile)
        lines.extend([line for line in reader][1:])
    start_urls = [('https://zh.wikipedia.org/zh-cn/{}'.format(urllib.quote(line[0])), line[2]) for line in lines]
    # start_urls = ['https://zh.wikipedia.org/zh-cn/%E5%91%A8%E6%9D%B0%E5%80%AB']


    def start_requests(self):
        for u, uid in self.start_urls:
            request = scrapy.Request(u, callback=self.parse_httpbin)
            request.meta['uuid'] = uid
            yield request

    def parse_httpbin(self, response):
        items = []
        item = SingerItem()
        # item['name'] = a_name
        html = bs4.BeautifulSoup(response.body, "html.parser")
        site = html.find("table", {"class": "infobox vcard plainlist"})
        if site is None:
            # items.append(item)
            return
        else:
            item['name'] = self.check_none_and_return_value(site.find('span', 'fn'))
            item['sex'] = self.check_none_and_return_value(site.find('th', class_='title role'))
            item['nickname'] = self.check_none_and_return_value(site.find('td', 'nickname'))
            item['nation'] = self.check_none_and_return_value(self.search_nation(site))
            item['category'] = self.check_none_and_return_value(self.search_category(site))
            item['uuid'] = response.meta['uuid']
            items.append(item)
        return items

    def check_none_and_return_value(self, data):
        if data is None:
            return None
        return data.get_text()

    def search_nation(self, data):
        right_tr = None
        for tr in data.find_all('tr'):
            th = tr.find('th')
            if th is not None:
                th_text = th.get_text()
                if th_text in [u'\u56fd\u7c4d']:
                    right_tr = tr
                    break
        if right_tr is None:
            return None
        td = right_tr.find('td', class_='category')
        return td

    def search_category(self, data):
        right_tr = None
        for tr in data.find_all('tr'):
            th = tr.find('th')
            if th is not None:
                th_text = th.get_text()
                if th_text in [u'\u97f3\u4e50\u7c7b\u578b']:
                    right_tr = tr
                    break
        if right_tr is None:
            return None
        td = right_tr.find('td', class_='category')
        return td



