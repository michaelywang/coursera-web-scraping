# -*- coding: utf-8 -*-

# Scrapy settings for coursera project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random

BOT_NAME = 'coursera'

SPIDER_MODULES = ['coursera.spiders']
NEWSPIDER_MODULE = 'coursera.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT ="+Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.187 Mobile Safari/534.11+"
# useful if you want to access a certain version of the website. Teacher gave us a pro-tip that we can use an older seeming device so it renders
# a simpler website that may have less JavaScript elements; makes xpaths and data easier to get sometimes.
# also can sometimes get past forbidden 403 or whatever errors.

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# whether you follow the websites rules for how you parse (delay times, etc)


#DOWNLOAD_DELAY = 3
DOWNLOAD_DELAY = 5.0
# how many seconds you want to wait between requests.
# if you need the website to download slower to fully load all parts, use this.

ITEM_PIPELINES = {'coursera.pipelines.WriteItemPipeline': 300}
# if you have multiple pipelines, you put them in order here in a dictionary style
# the number doesn't really matter, just relative to other items
# lower number goes first, counts upward in order the functions run in the pipeline
# if you only have one (like I do here), doesn't matter what you put there (under 999)

