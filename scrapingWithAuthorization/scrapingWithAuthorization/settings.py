# Scrapy settings for rutracker project

BOT_NAME = 'scrapingWithAuthorization'
SPIDER_MODULES = ['scrapingWithAuthorization.spiders']
NEWSPIDER_MODULE = 'scrapingWithAuthorization.spiders'
ITEM_PIPELINES = ['scrapingWithAuthorization.pipelines.JsonWithEncodingPipeline']
DOWNLOAD_DELAY = 1