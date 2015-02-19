# -*- coding: utf-8 -*-

# Scrapy settings for vk project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'vk'

SPIDER_MODULES = ['vk.spiders']
NEWSPIDER_MODULE = 'vk.spiders'

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.4.0"

ITEM_PIPELINES = {
    'vk.pipelines.JsonWriterPipeline': 100,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'vk (+http://www.yourdomain.com)'
