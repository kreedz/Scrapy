import scrapy
from habrahabr.items import HabrahabrItem
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Request


class HabrSpider(CrawlSpider):
    name = 'habr'
    allowed_domains = ['habrahabr.ru', 'habrastorage.org']
    start_urls = ['http://habrahabr.ru/']

    rules = (
        Rule(LxmlLinkExtractor(restrict_xpaths=('.//h1/a[@class="post_title"]')), callback='parse_item'),
        Rule(LxmlLinkExtractor(restrict_xpaths=('.//*[@id="nav-pages"]/li/a')), follow=True),
    )

    #def parse_start_url(self, response):
        #return Request(HabrSpider.start_urls[0], callback=self.parse_item)

    def parse_item(self, response):
        xpath = './/div[substring(@class, string-length(@class) - string-length("shortcuts_item") + 1) = "shortcuts_item"]'
        for sel in response.xpath(xpath):
            l = ItemLoader(item=HabrahabrItem(), selector=sel, response=response)
            l.add_xpath('title', 'h1/span/text()')
            l.add_xpath('image_urls', 'div[@class="content html_format"]/img/@src')
            yield l.load_item()
