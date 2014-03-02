# Scrapy settings for scrapingWithProxies project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapingWithProxies'

SPIDER_MODULES = ['scrapingWithProxies.spiders']
NEWSPIDER_MODULE = 'scrapingWithProxies.spiders'
ITEM_PIPELINES = ['scrapingWithProxies.pipelines.JsonWithEncodingPipeline']

PROXIES = [{'ip_port': 'PROXY_IP:PORT_NUMBER', 'user_pass': ''}, ]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'scrapingWithProxies.middlewares.ProxyMiddleware': 100,
}
