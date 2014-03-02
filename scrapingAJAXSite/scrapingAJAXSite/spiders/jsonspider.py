from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapingAJAXSite.items import scrapingAJAXSiteItem
import json


class scrapingAJAXSiteSpider(CrawlSpider):
    name = 'scrapingAJAXSite'
    allowed_domains = ['angel.co']
    urls_to_parse = ['https://angel.co/public?page=%s' % page for page in xrange(2, 10)]

    def start_requests(self):
        for url in self.urls_to_parse:
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        jsonResponse = json.loads(response.body)
        hxs = Selector(text=jsonResponse['html'])
        divs = hxs.xpath("//div[@class='name']/a/text()")
        items = []
        for div in divs:
            item = scrapingAJAXSiteItem()
            item['name'] = div.extract()
            items.append(item)
        return items