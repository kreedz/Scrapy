from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from habrahabr.items import HabrahabrItem


class HabrSpider(CrawlSpider):
    name = "habr"
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
            item = HabrahabrItem()
            item['id'] = div.xpath("//div[@class='published']/following-sibling::h1/a/@href").re(r'\d+')[i]
            item['name'] = div.xpath("//div[@class='published']/following-sibling::h1/a/text()").extract()[i]
            item['date'] = div.xpath("//div[@class='published']/text()").extract()[i]
            item['review'] = div.xpath(
                "//div[@class='published']/following-sibling::div/div/div[@class='pageviews']/text()").extract()[i]
            item['selected'] = div.xpath(
                "//div[@class='published']/following-sibling::div/div/div[@class='favs_count']/text()").extract()[i]
            item['author'] = div.xpath(
                "//div[@class='published']/following-sibling::div/div/div[@class='author']/a/text()").extract()[i]
            item['url'] = div.xpath("//div[@class='published']/following-sibling::h1/a/@href").extract()[i]
            i += 1
            items.append(item)
        return items