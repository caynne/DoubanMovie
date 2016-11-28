# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json,os,codecs
from scrapy import signals
from scrapy.contrib.exporter import JsonLinesItemExporter
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

filename = os.path.abspath(os.curdir) + '/MrDonkey.csv'

class DoubanmoviePipeline(object):
    # def __init__(self):
    #     self.file = codecs.open(filename,'wb',encoding='utf-8')
    #
    # def process_item(self, item, spider):
    #     line = json.dumps(dict(item)) + "\n"
    #     self.file.write(line.decode("unicode_escape"))
    #     return item

    def write_to_csv(self,item):
        csvwriter = csv.writer(codecs.open(filename,'a',encoding='utf-8'))
        print '***************************************'
        print '准备写入csv'
        csvwriter.writerow([item[key] for key in item.keys()])
        print '已写入csv'

    def process_item(self,item,spider):
        self.write_to_csv(item)
        return item