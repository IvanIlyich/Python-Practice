# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
from scrapy import signals
import json, codecs


class XPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingWiki(object):
    def __init__(self):
        self.file = codecs.open('papers.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        name = json.dumps(str(item['name']), ensure_ascii=False) + u','
        sex = json.dumps(str(item['sex']), ensure_ascii=False) + u','
        nickname = json.dumps(str(item['nickname']), ensure_ascii=False) + u','
        nation = json.dumps(str(item['nation']), ensure_ascii=False) + u','
        category = json.dumps(str(item['category']), ensure_ascii=False) + u','
        uuid = json.dumps(str(item['uuid']), ensure_ascii=False)
        line = name + sex + nickname + nation + category + uuid +'\n'
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
