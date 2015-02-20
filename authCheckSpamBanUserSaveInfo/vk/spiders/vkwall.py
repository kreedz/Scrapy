# -*- coding: utf-8 -*-

from scrapy.http import Request, FormRequest
from scrapy import log
from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose
from vk.items import VkItem, normalize_date

import codecs
import os
import json
import locale
from datetime import datetime, date, timedelta


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

def get_spam_words_from_file(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return [spaw_word.strip() for spaw_word in f.readlines()]

def get_spam_words_from_msg(text, spam_words_file):
    if text:
        text = text[0]
    spam_words = []
    for spam_word in get_spam_words_from_file(spam_words_file):
        if spam_word in text:
            spam_words.append(spam_word)
    return spam_words

def get_auth_data(filename):
    with open(filename, 'r') as f:
        return json.loads(f.readline())

def get_last_date_to_parse(days):
    return datetime.now().date() - timedelta(days=days)

def is_date_less_last_date(date, days_to_last_date):
    return datetime.strptime(date.encode('utf-8'), '%d %b %y').date() < get_last_date_to_parse(days_to_last_date)


class VkwallSpider(InitSpider):
    name = 'vkwall'
    allowed_domains = ['vk.com']
    start_urls = ['https://vk.com/scrapytest']
    login_page = 'https://vk.com/login.php'

    txt_dir = 'txt'
    spam_words_file = os.path.join(txt_dir, 'spam_words.txt')
    auth_data = os.path.join(txt_dir, 'auth_data.txt')

    days_count_to_parse = 5

    def init_request(self):
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        return FormRequest.from_response(
            response,
            formxpath='//form[@id="login"]',
            formdata=get_auth_data(self.auth_data),
            callback=self.after_login
        )

    def after_login(self, response):
        if not 'feed' in response.url:
            self.log('Login failed', level=log.ERROR)
            return
        self.log('Login Successful. Parsing all other URLs')
        return self.initialized()

    def parse(self, response):
        sel = response.xpath('.//*[@class="post_info"]')
        if not sel:
            self.log('posts are not find')
            return
        for s in sel:
            wall_text = s.xpath('div[@class="wall_text"]')
            text = wall_text.xpath('div/div[@class="wall_post_text"]').extract()
            spam_words = get_spam_words_from_msg(text, self.spam_words_file)
            if spam_words:
                l = ItemLoader(item=VkItem(), selector=s, response=response)
                date = s.xpath('div[@class="replies"]/div/small/a[1]/span/text()').extract()
                date = l.get_value(date, MapCompose(normalize_date), TakeFirst())
                if is_date_less_last_date(date, self.days_count_to_parse):
                    return
                l.add_value('id', wall_text.xpath('div/a/@data-from-id').extract())
                l.add_value('name', wall_text.xpath('div/a/text()').extract())
                l.add_value('text', text)
                l.add_value('date', date)
                l.add_value('words', spam_words)
                yield l.load_item()
                #yield Request(get_posts_url, callback=self.parse)
