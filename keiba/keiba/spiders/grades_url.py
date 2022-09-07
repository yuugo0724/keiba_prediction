import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from keiba.items import KeibaItem

class GradesUrlSpider(scrapy.Spider):
    name = 'grades_url'
    allowed_domains = ['www.jra.go.jp']
    start_urls = ['https://www.jra.go.jp/datafile/seiseki/']
    comp_url = 'https://www.jra.go.jp'
    old_comp_url = 'https://www.jra.go.jp/datafile/seiseki/'
    urls = []


    def parse(self, response):
        t_urls = response.css("ul[class='link_list multi div2 center mt15'] a::attr(href)").extract()
        urls = [self.comp_url + i for i in t_urls]
        print("==================================================")
        print("■1回目URL取得")
        print("==================================================")
        print(urls)
        for url in urls:
            yield scrapy.Request(url, self.GradesCurrentUrl)

    def GradesCurrentUrl(self, response):
        sel = Selector(response)
        url_list = [self.comp_url + i for i in sel.css("td[class='result'] a[class='btn-def btn-xs']::attr(href)").extract()]
        print("==================================================")
        print("■2回目カレントURL取得")
        print("==================================================")
        print(url_list)
        with open("grades_urls.txt", "a", encoding = 'UTF-8') as f:
            [f.write(i+"\n") for i in url_list]
        urls = [self.comp_url + i for i in sel.css("div[class='year_select_area'] div[class='dropdown'] select[class='dropdown-select bn-list'] option::attr(value)").extract()]
        del urls[0]
        print("==================================================")
        print("■2回目URL取得")
        print("==================================================")
        print(urls)
        for url in urls:
            yield scrapy.Request(url, self.GradesPastUrl)
        
    def GradesPastUrl(self, response):
        sel = Selector(response)
        item = KeibaItem()
        url_list = [self.comp_url + i for i in sel.css("td[class='result'] a[class='btn-def btn-xs']::attr(href)").extract()]
        print("==================================================")
        print("■デバッグ(url_list表示)")
        print("==================================================")
        print(url_list)
        if not url_list:
            print("■条件分岐テスト")
            url_list = [self.old_comp_url + i.replace('../../','') for i in sel.css("td[class='gray12'] a::attr(href)").extract() if '/result/' in i]
        print("==================================================")
        print("■3回目URL取得")
        print("==================================================")
        print(url_list)
        with open("grades_urls.txt", "a", encoding = 'UTF-8') as f:
            [f.write(i+"\n") for i in url_list]
        

