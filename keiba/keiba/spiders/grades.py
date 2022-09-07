from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from keiba.items import KeibaItem


class GradesSpider(CrawlSpider):
    name = 'grades'
    allowed_domains = ['www.jra.go.jp']
    start_urls = ['https://www.jra.go.jp/']
    allow_list = ['https://www.jra.go.jp/datafile/seiseki/replay/\d\d\d\d/001.html']

    def parse(self, response):
        sel = Selector(response)
        item = KeibaItem()
        item_urls = [self.comp_url + i for i in sel.css("td[class='result'] a[class='btn-def btn-xs']::attr(href)").extract()]
