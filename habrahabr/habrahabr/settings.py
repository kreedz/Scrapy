# -*- coding: utf-8 -*-

# Scrapy settings for habrahabr project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'habrahabr'

SPIDER_MODULES = ['habrahabr.spiders']
NEWSPIDER_MODULE = 'habrahabr.spiders'

ITEM_PIPELINES = {
    'habrahabr.pipelines.JsonWriterPipeline': 100,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'habrahabr (+http://www.yourdomain.com)'
