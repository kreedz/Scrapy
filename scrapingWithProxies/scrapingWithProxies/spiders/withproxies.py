from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapingWithProxies.items import TestItem


class TestProxiesSpider(CrawlSpider):
    name = "testproxies"
    allowed_domains = ["habrahabr.ru"]
    start_urls = ["http://habrahabr.ru/page%s" % page for page in xrange(1, 4)]

    rules = (
        Rule(SgmlLinkExtractor(allow=('page')), callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = Selector(response)
        divs = hxs.xpath("//div[@class='posts shortcuts_items']/div")
        items = []
        i = 0
        for div in divs:
            item = TestItem()
            item['id'] = div.xpath("//div[@class='published']/following-sibling::h1/a/@href").re(r'\d+')[i]
            i += 1
            items.append(item)
        return items