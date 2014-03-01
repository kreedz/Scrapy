from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy import log
from scrapy.selector import Selector
from scrapingWithAuthorization.items import RutrackerItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


class RutrackerSpider(CrawlSpider):
    name = "rutracker"
    # URL for the login page
    login_page = 'http://login.rutracker.org/forum/login.php'
    # Array of pages to goto after logging i
    urls_to_parse = ['http://rutracker.org/forum/viewforum.php?f=2093&start=50']

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'viewtopic\.php\?t=\d+$')), callback='parse_item'),
    )

    def start_requests(self):
        yield Request(
            url=self.login_page,
            callback=self.login,
            dont_filter=True
        )

    def login(self, response):
        return FormRequest.from_response(
            response,
            formxpath="//form[@id='login-form']",
            formdata={'login_username': 'your_login', 'login_password': 'your_password'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if not "your_login" in response.body:
            self.log("Login failed", level=log.ERROR)
            return

        self.log('Login Successful. Parsing all other URLs')
        for url in self.urls_to_parse:
            # Result of these requests will be in parse function
            yield self.make_requests_from_url(url)

    def parse_item(self, response):
        # All subsequent requests come here
        hxs = Selector(response)
        print "parse"
        items = []
        item = RutrackerItem()
        item["name"] = hxs.xpath("//h1[@class='maintitle']/a/text()").extract()[0]
        item['seed'] = hxs.xpath("//span[@class='seed']/b/text()").extract()[0]
        items.append(item)
        return items