# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time
from my_dump import dump
class NewsPipeline(object):
    count=0
    def process_item(self, item, spider):
        self.count+=1
        print spider.name
        timearray = time.strptime(item['time'], "%Y-%m-%d %H:%M:%S")
        data=dict()
        item['ctime'] = time.mktime(timearray)
        if self.count>=5000:
            spider.crawler.engine.close_spider(spider, 'Jobs Done!')
        data['imgs']=item['imgs']
        data['title']=item['title']
        data['ctime']=item['ctime']
        data['time']=item['time']
        data['content']=item['content']
        data['url']=item['url']
        f=dump(spider.name+str(self.count)+'.pkl',data)
        print self.count
        return item
