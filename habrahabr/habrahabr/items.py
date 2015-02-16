# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item
from scrapy.contrib.loader.processor import TakeFirst, MapCompose
from w3lib.html import remove_tags


def join_http_scheme(value):
    if not (value.startswith('http://') or value.startswith('https://')):
        return "http:" + value
    return value

def strip_wrap(value):
    return value.strip()


class HabrahabrItem(Item):
    title = Field(output_processor=TakeFirst())
    comments = Field()
    image_urls = Field(input_processor=MapCompose(join_http_scheme))
    images = Field()


class HabrahabrComment(Item):
    comment = Field(input_processor=MapCompose(remove_tags, strip_wrap), output_processor=TakeFirst())
    habrahabr = Field()
