import scrapy
from habrahabr.items import HabrahabrItem
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Request


class HabrSpider(CrawlSpider):
    name = "habr"
    allowed_domains = ["habrahabr.ru"]
    start_urls = ["http://habrahabr.ru"]

    rules = (
        Rule(LxmlLinkExtractor(restrict_xpaths=('.//*[@id="nav-pages"]/li/a')), callback='parse_item'),
    )

    def parse_start_url(self, response):
        return Request(HabrSpider.start_urls[0], callback=self.parse_item)

    def parse_item(self, response):
        xpath = './/div[substring(@class, string-length(@class) - string-length("shortcuts_item") + 1) = "shortcuts_item"]'
        for sel in response.xpath(xpath):
            #item = HabrahabrItem()
            #item['title'] = t(sel.xpath('h1/a[1]/text()').extract())
            #item['link'] = sel.xpath('string(h1/a/@href)').extract()
            #item['tags'] = sel.xpath('div/a[substring(@class, 1, string-length("hub")) = "hub"]/text()').extract()
            #infopanel_wrapper = sel.xpath('div[@class="infopanel_wrapper"]/div')
            #item['views'] = infopanel_wrapper.xpath('div[@class="pageviews"]/text()').extract()
            #item['favorites'] = infopanel_wrapper.xpath('div[@class="favs_count"]/text()').extract()
            #item['author'] = infopanel_wrapper.xpath('div[@class="author"]/a/text()').extract()
            #yield item
            print response.url
            l = ItemLoader(item=HabrahabrItem(), selector=sel, response=response)
            l.add_xpath('title', 'h1/a[1]/text()')
            yield l.load_item()
