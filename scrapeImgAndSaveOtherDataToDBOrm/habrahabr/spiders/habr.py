#import scrapy
from habrahabr.items import HabrahabrItem, HabrahabrComment
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Request
from scrapy import log


class HabrSpider(CrawlSpider):
    name = 'habr'
    allowed_domains = ['habrahabr.ru', 'habrastorage.org']
    start_urls = ['http://habrahabr.ru/']

    rules = (
        Rule(LxmlLinkExtractor(restrict_xpaths=('.//h1/a[@class="post_title"]')), callback='parse_item'),
        Rule(LxmlLinkExtractor(restrict_xpaths=('.//*[@id="nav-pages"]/li/a')), follow=True),
    )

    def __init__(self, category=None, *args, **kwargs):
        super(HabrSpider, self).__init__(*args, **kwargs)
        log.ScrapyFileLogObserver(open('debug.log', 'w'), level=log.DEBUG).start()
        log.ScrapyFileLogObserver(open('error.log', 'w'), level=log.ERROR).start()

    def parse_item(self, response):
        xpath = './/div[@class="content_left"]'
        sel = response.xpath(xpath)
        if not sel:
            return
        l = ItemLoader(item=HabrahabrItem(), selector=sel, response=response)
        l.add_xpath('title', '//h1/span/text()')
        l.add_xpath('image_urls', '//div[@class="content html_format"]/img/@src')
        comments_items = []
        comments = sel.xpath('//div[starts-with(@class, "message html_format")]').extract()
        for comment in comments:
            comment_item = ItemLoader(item=HabrahabrComment(), selector=sel, response=response)
            comment_item.add_value('comment', comment)
            comments_items.append(comment_item.load_item())
        l.add_value('comments', comments_items)
        yield l.load_item()
