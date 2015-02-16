# -*- coding: utf-8 -*-

# Scrapy settings for habrahabr project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

BOT_NAME = 'habrahabr'

SPIDER_MODULES = ['habrahabr.spiders']
NEWSPIDER_MODULE = 'habrahabr.spiders'

ITEM_PIPELINES = {
    #'habrahabr.pipelines.JsonWriterPipeline': 100,
    'habrahabr.pipelines.HabrahabrPipeline': 100,
    'habrahabr.pipelines.MyImagesPipeline': 1,
}

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGES_STORE = os.path.join(BASE_DIR, 'images')

IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}

IMAGES_EXPIRES = 90

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'kreedz',
    'password': '',
    'database': 'scrape'
}

DOWNLOAD_DELAY = 0.5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'habrahabr (+http://www.yourdomain.com)'
