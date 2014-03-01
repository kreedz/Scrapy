# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class HabrahabrItem(Item):
    id = Field()
    name = Field()
    date = Field()
    review = Field()
    selected = Field()
    author = Field()
    url = Field()
