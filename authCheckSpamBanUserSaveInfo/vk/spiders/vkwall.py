# -*- coding: utf-8 -*-

from scrapy.http import Request, FormRequest, Response, HtmlResponse
from scrapy import log
from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose
from vk.items import VkItem, normalize_date

import codecs
import os
import json
import locale
import re
import urllib
from datetime import datetime, date, timedelta
from random import randrange


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

def get_spam_words_from_file(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return [spaw_word.strip() for spaw_word in f.readlines()]

def get_spam_words_from_msg(text, spam_words_from_file):
    if text:
        text = text[0]
    spam_words = []
    for spam_word in spam_words_from_file:
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

def get_url_hided_replies(js_str, main_page):
    rnd = str(randrange(1, 100000))
    post_id = js_str[js_str.find("'")+1 : js_str.rfind("'")]
    params = {
        "_rndVer": rnd,
        "act": "get_replies",
        "al":"-1",
        "cont": "replies" + post_id,
        "count": "false",
        "post": post_id
    }
    return main_page + '/al_wall.php?' + urllib.urlencode(params)


class VkwallSpider(InitSpider):
    name = 'vkwall'
    allowed_domains = ['vk.com']
    main_page = 'https://' + allowed_domains[0]
    start_urls = [main_page + '/scrapytest']
    login_page = main_page + '/login.php'

    txt_dir = 'txt'
    spam_words_from_file = get_spam_words_from_file(os.path.join(txt_dir, 'spam_words.txt'))
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
            spam_words = get_spam_words_from_msg(text, self.spam_words_from_file)
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
                #ban => Request()
            replies_hidden = s.xpath('.//a[@class="wr_header"]/@onclick')
            if replies_hidden:
                url = get_url_hided_replies(replies_hidden[0].extract(), self.main_page)
                yield Request(url=url, callback=self.get_hided_items)
            else:
                replies = s.xpath('.//div[@class="reply_table"]').extract()
                for reply in replies:
                    raw_html = ''.join(reply.splitlines()).encode('utf-8')
                    html_response = HtmlResponse(url=response.url, body=raw_html)
                    for i in self.get_replies_items(html_response):
                        yield i.load_item()
            #yield Request(get_posts_url, callback=self.parse)

    def get_hided_items(self, response):
        for i in self.get_replies_items(response):
            yield i.load_item()

    def get_replies_items(self, response):
        regex = ur'id.{2,3}reply_delete-([\d_]+?)\\?".+?data-from-id.{2,3}?([\d\-]+?)''\\?".*?\>(.+?)\<\\?/a\>' \
                '.+?wall_reply_text.{1,2}\>?(.+?)\<\\?/div\>.+?rel_date.*?"\>(.+?)\<\\?/span\>'
        m = re.finditer(regex, response.body_as_unicode())
        import ipdb; ipdb.set_trace()
        items = []
        for i in m:
            text = i.group(4)
            spam_words = get_spam_words_from_msg([text], self.spam_words_from_file)
            if spam_words:
                l = ItemLoader(item=VkItem(), response=response)
                l.add_value('id', i.group(2))
                l.add_value('name', i.group(3))
                l.add_value('text', text)
                l.add_value('date', l.get_value(i.group(5), MapCompose(normalize_date), TakeFirst()))
                l.add_value('words', spam_words)
                items.append(l)
        return items
