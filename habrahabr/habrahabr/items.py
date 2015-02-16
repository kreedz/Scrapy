# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item
from scrapy.contrib.loader.processor import TakeFirst


class HabrahabrItem(Item):
    title = Field(output_processor=TakeFirst())
    #link = Field(output_processor=TakeFirst())
    #tags = Field()
    #views = Field(output_processor=TakeFirst())
    #favorites = Field(output_processor=TakeFirst())
    #author = Field(output_processor=TakeFirst())
