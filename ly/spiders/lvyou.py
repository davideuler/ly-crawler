# -*- coding: utf-8 -*-
import scrapy
import urlparse
from ly.items import LyItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request


class LvyouSpider(scrapy.Spider):
    name = "lvyou"
    allowed_domains = ["ly.com","17u.com","17u.net"]
    start_urls = (
        'http://www.ly.com/notexist.html',
    )

    download_delay = 1

    rules = (
        # Extract all links and follow links from them 
        # (since no callback means follow=True by default)
        # (If "allow" is not given, it will match all links.)
        Rule(SgmlLinkExtractor(allow=()), follow=True),
    
        # Extract links matching the "ad/any-words/67-anynumber.html" pattern
        # and parse them with the spider's method parse_item (NOT FOLLOW THEM)
        #Rule(SgmlLinkExtractor(allow=r'ad/.+/67-\d+\.html'), callback='parse_item'),
    )
    
    def log(self,msg):
        print(msg)

    def parse(self, response):
        item = LyItem()
        item['url'] = response.url
        item['title'] = response.xpath("/html/head/title/text()").extract()[0]
        item['status'] = response.status
        item['length'] = len(response.body)
        item['date'] = response.headers.get('Date')
        item['latency'] = response.meta.get('download_latency')
        yield item
        for link in response.xpath("//*/a/@href").extract():
            itemLink = urlparse.urljoin(response.url, link)
            self.log('Found item link: %s' % itemLink)
            yield Request(itemLink, callback = self.parse)
