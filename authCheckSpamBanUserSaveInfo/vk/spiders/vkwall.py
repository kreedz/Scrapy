# -*- coding: utf-8 -*-

from scrapy.http import Request, FormRequest
from scrapy import log
from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.loader import ItemLoader
from vk.items import VkItem

import codecs
import os
import json


def get_spam_words(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return [spaw_word.strip() for spaw_word in f.readlines()]

def get_auth_data(filename):
    with open(filename, 'r') as f:
        return json.loads(f.readline())


class VkwallSpider(InitSpider):
    name = 'vkwall'
    allowed_domains = ['vk.com']
    start_urls = ['https://vk.com/scrapytest']
    login_page = 'https://vk.com/login.php'

    txt_dir = 'txt'
    spam_words = get_spam_words(os.path.join(txt_dir, 'spam_words.txt'))
    auth_data = os.path.join(txt_dir, 'auth_data.txt')

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
            spam_words = self.get_spam_words(text)
            if spam_words:
                l = ItemLoader(item=VkItem(), selector=s, response=response)
                l.add_value('id', wall_text.xpath('div/a/@data-from-id').extract())
                l.add_value('name', wall_text.xpath('div/a/text()').extract())
                l.add_value('text', text)
                l.add_xpath('date', 'div[@class="replies"]/div/small/a[1]/span/text()')
                l.add_value('words', spam_words)
                yield l.load_item()
                #yield Request(get_posts_url, callback=self.parse)

    def get_spam_words(self, text):
        if text:
            text = text[0]
        spam_words = []
        for spam_word in self.spam_words:
            if spam_word in text:
                spam_words.append(spam_word)
        return spam_words
