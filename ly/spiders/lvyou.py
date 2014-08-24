# -*- coding: utf-8 -*-
import scrapy
import urlparse
from ly.items import LyItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals



class LvyouSpider(BaseSpider):
    name = "lvyou"
    handle_httpstatus_list = [403,404,500,502,503,504]
    allowed_domains = ["ly.com","17u.com","17u.net"]
    start_urls = (
        'http://www.ly.com/',
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

    def __init__(self, category=None):
        self.failed_urls = []

    def log(self,msg):
        print(msg)

    def parse(self, response):
        if response.status in self.handle_httpstatus_list:
            self.crawler.stats.inc_value('failed_url_count')
            self.failed_urls.append(response.url)
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

    def handle_spider_closed(spider, reason):
        #stats.set_value('failed_urls', ','.join(spider.failed_urls))
        print(spider.failed_urls)

    def process_exception(self, response, exception, spider):
        ex_class = "%s.%s" % (exception.__class__.__module__, exception.__class__.__name__)
        self.crawler.stats.inc_value('downloader/exception_count', spider=spider)
        self.crawler.stats.inc_value('downloader/exception_type_count/%s' % ex_class, spider=spider)

    dispatcher.connect(handle_spider_closed, signals.spider_closed)

