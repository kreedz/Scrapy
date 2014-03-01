# Define here the models for your scraped items

from scrapy.item import Item, Field


class RutrackerItem(Item):
    name = Field()
    seed = Field()
