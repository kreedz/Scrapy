# Scrapy settings for habrahabr project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapingSimpleSite'

SPIDER_MODULES = ['scrapingSimpleSite.spiders']
NEWSPIDER_MODULE = 'scrapingSimpleSite.spiders'
ITEM_PIPELINES = ['scrapingSimpleSite.pipelines.JsonWithEncodingPipeline']
