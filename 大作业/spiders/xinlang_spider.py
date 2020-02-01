# -*- coding:utf-8 -*-
import scrapy
from ..items import *
import re
from urlparse import urljoin

class XinlangSpider(scrapy.Spider):
    name = "xinlang"
    allowed_domains = ["sports.sina.com.cn","sports.sina.cn"]
    start_urls = [
            "http://sports.sina.com.cn/"
    ]
    count=0

    def parse(self, response):

        urls=response.xpath('//a/@href').extract()
        title=response.xpath('//title/text()').extract()[0]
        content="".join(response.xpath('//*[@id="artibody" or @id="article" or @id="article_content"]//p/text()').extract())
        if content:
            content = re.sub(r'\u3000', '', content)
            content = re.sub(r'[ \xa0?]+', ' ', content)
            content = re.sub(r'\s*\n\s*', '\n', content)
            content = re.sub(r'\s*(\s)', r'\1', content)
            content = ''.join([x.strip() for x in content])
            time=response.xpath('//span[@class="date"]/text()').extract()
            if not time:
                time=response.xpath('//span[@id="pub_date"]/text()').extract()
                if not time:
                    return 
                time=time[0].strip()
                time=time[0:4]+'-'+time[5:7]+'-'+time[8:10]+' '+time[11:13]+':'+time[14:16]+':00'
                print time
            else:
                time=time[0].strip()
                time=time[0:4]+'-'+time[5:7]+'-'+time[8:10]+' '+time[12:14]+':'+time[15:17]+':00'
            item = NewsItem()
            imgs=response.xpath('//div[@class="img_wrapper"]//img/@src').extract()
            for i in range(len(imgs)):
                imgs[i]=urljoin(response.url,imgs[i])
            print response.url
            print time
            print title
            item['imgs']=imgs
            item['content']=content
            item['url']=response.url
            item['title']=title
            item['time']=time
            self.count+=1
            yield item
        for url in urls:
            if 'match.sports.sina.com.cn' in response.url:
                continue
            if 'cba.sports.sina.com.cn' in response.url:
                continue
            if 'nba.sports.sina.com.cn' in response.url:
                continue
            if 'tags.sports.sina.com.cn' in response.url:
                continue
            if 'sports.sina.com.cn/photo_xh' in response.url:
                continue
            url=urljoin(response.url,url)
            yield scrapy.Request(url, callback=self.parse)
