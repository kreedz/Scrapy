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
        return today.strftime(date_format).decode('utf-8')
    p = re.compile(ur'вчера', re.UNICODE)
    if p.match(date):
        return (today - timedelta(days=1)).strftime(date_format).decode('utf-8')
    p = re.compile(ur'(\d{1,2})\s(\w{3})\s(?:(в)\s\d{1,2}:\d{2}|(\d{4}))', re.UNICODE)
    m = p.match(date)
    if m:
        date = m.group(1) + ' ' +  m.group(2) + ' '
        if m.group(3) is None:
            date += m.group(4)[2:]
        else:
            date += str(datetime.now().year % 100)
    first_month_char = date[date.find(' ') + 1]
    return date.replace(first_month_char, first_month_char.upper())


class VkItem(Item):
    id = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())
    text = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    date = Field(output_processor=TakeFirst())
    words = Field()
