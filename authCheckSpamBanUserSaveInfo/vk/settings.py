# -*- coding: utf-8 -*-

BOT_NAME = 'vk'

SPIDER_MODULES = ['vk.spiders']
NEWSPIDER_MODULE = 'vk.spiders'

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.4.0"

ITEM_PIPELINES = {
    'vk.pipelines.JsonWriterPipeline': 100,
}

COOKIES_DEBUG = True
