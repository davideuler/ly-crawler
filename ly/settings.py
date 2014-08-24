# -*- coding: utf-8 -*-

# Scrapy settings for ly project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ly'

SPIDER_MODULES = ['ly.spiders']
NEWSPIDER_MODULE = 'ly.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ly (+http://www.yourdomain.com)'
#USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22 AlexaToolbar/alxg-3.1"
#download_delay = 1
    
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'ly.rotate_useragent.RotateUserAgentMiddleware' :400
    }