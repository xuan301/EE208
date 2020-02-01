import scrapy
from ..items import *
import re
from urlparse import urljoin

class WangyiSpider(scrapy.Spider):
    name = "wangyi"
    allowed_domains = ["sports.163.com"]
    start_urls = [
            "https://sports.163.com/"
    ]
    count=0

    def parse(self, response):
        urls=response.xpath('//a/@href').extract()
        title=response.xpath('//title/text()').extract()[0]
        time=response.xpath('//div[@class="post_time_source"]/text()').extract()
        print response.url
        if time:
            content="".join(response.xpath('//div[@class="post_body"]//p/text()').extract())
            content = re.sub(r'\u3000', '', content)
            content = re.sub(r'[ \xa0?]+', ' ', content)
            content = re.sub(r'\s*\n\s*', '\n', content)
            content = re.sub(r'\s*(\s)', r'\1', content)
            content = ''.join([x.strip() for x in content])
            item = NewsItem()
            imgs=response.xpath('//div[@class="post_body"]//img/@src').extract()
            for i in range(len(imgs)):
                imgs[i]=urljoin(response.url,imgs[i])
            print response.url
            time=time[0].strip()[:19]
            print time
            print title
            #print content
            item['imgs']=imgs
            item['content']=content
            item['url']=response.url
            item['title']=title
            item['time']=time
            self.count+=1
            yield item
        for url in urls:
            url=urljoin(response.url,url)
            if 'goal.sports.163.com' in url:
                continue
            if 'cba.sports.163.com' in url:
                continue
            if 'nba.sports.163.com' in response.url:
                continue
            if 'cs.sports.163.com' in response.url:
                continue
            if 'photoview' in response.url:
                continue
            if 'wiki.sports.163.com' in url:
                continue
            yield scrapy.Request(url, callback=self.parse)
