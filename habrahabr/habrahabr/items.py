# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item
from scrapy.contrib.loader.processor import TakeFirst, MapCompose


def join_http_scheme(value):
    if not (value.startswith('http://') or value.startswith('https://')):
        return "http:" + value
    return value


class HabrahabrItem(Item):
    title = Field(output_processor=TakeFirst())
    #link = Field(output_processor=TakeFirst())
    #tags = Field()
    #views = Field(output_processor=TakeFirst())
    #favorites = Field(output_processor=TakeFirst())
    #author = Field(output_processor=TakeFirst())
    image_urls = Field(input_processor=MapCompose(join_http_scheme))
    images = Field()
