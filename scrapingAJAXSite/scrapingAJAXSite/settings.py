# Scrapy settings for scrapingAJAXSite project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapingAJAXSite'

SPIDER_MODULES = ['scrapingAJAXSite.spiders']
NEWSPIDER_MODULE = 'scrapingAJAXSite.spiders'
ITEM_PIPELINES = ['scrapingAJAXSite.pipelines.JsonWithEncodingPipeline']
