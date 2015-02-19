# -*- coding: utf-8 -*-

from scrapy.item import Field, Item
from scrapy.contrib.loader.processor import TakeFirst, MapCompose
from w3lib.html import remove_tags

from datetime import datetime, timedelta
import re
import locale


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

def normalize_date(date):
    today = datetime.now().date()
    date_format = '%d %b %y'
    p = re.compile(ur'((\S+?\s)?(минут|час)\S{,2}\sназад)|сегодня.*', re.UNICODE)
    if p.match(date):
        return today.strftime(date_format).decode('utf-8').lower()
    p = re.compile(r'вчера')
    if p.match(date):
        return (today - timedelta(days=1)).strftime(date_format).decode('utf-8').lower()
    return date


class VkItem(Item):
    id = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())
    text = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    date = Field(input_processor=MapCompose(normalize_date), output_processor=TakeFirst())
    words = Field()
