import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from grades.items import GradesItem
#from functools import partial

class GradesUrlSpider(scrapy.Spider):
    name = 'two_years_ago'
    allowed_domains = ['www.jra.go.jp']
    start_urls = ['https://www.jra.go.jp/datafile/seiseki/']
    comp_url = 'https://www.jra.go.jp'
    grades_comp_url = 'https://www.jra.go.jp/datafile/seiseki/'
    
    def parse(self, response):
        sel = Selector(response)
        urls = sel.css("ul[class='link_list multi div2 center mt15'] a::attr(href)").extract()
        current_urls = [self.comp_url + i for i in urls]
        print("==================================================")
        print("■重賞レース・GIレースの遷移用URL取得")
        print("==================================================")
        for url in current_urls:
            print(url)
            yield scrapy.Request(url, self.tran_url)

    def tran_url(self, response):
        sel = Selector(response)
        #url_list = [self.comp_url + i for i in sel.css("td[class='result'] a[class='btn-def btn-xs']::attr(href)").extract()]
        print("==================================================")
        print("■年度別、重賞レース・GIレースの遷移用URL取得")
        print("==================================================")
        #print(url_list)
        #with open("grades_urls.txt", "a", encoding = 'UTF-8') as f:
        #    [f.write(i+"\n") for i in url_list]
        tran_urls = [self.comp_url + i for i in sel.css("div[class='year_select_area'] div[class='dropdown'] select[class='dropdown-select bn-list'] option::attr(value)").extract()]
        del tran_urls[0]
        #print(tran_urls)
        for url in tran_urls:
            print(url)
            yield scrapy.Request(url, self.grades_url)
        
    def grades_url(self, response):
        sel = Selector(response)
        base_url = str(response.request.url)
        item = GradesItem()
        grades_url = [self.comp_url + i for i in sel.css("td[class='result'] a[class='btn-def btn-xs']::attr(href)").extract()]
        print("==================================================")
        print("■年度別、重賞レース・GIレースのレース結果URL取得")
        print("base_url: " + base_url)
        print("==================================================")
        #print(grades_url)
        for url in grades_url:
            print(url)
        """
        古い年度のレース結果はhtmlのclassがresultではない
        そのためurl_listが空で帰ってきたときは、別でセレクタを作って取得する
        """
        if not grades_url:
            print("==================================================")
            print("■年度別、重賞レース・GIレースのレース結果URL取得(url整形版)")
            print("==================================================")
            urls = sel.css("td[class='gray12'] a::attr(href)").extract()
            # うまく動かないため、for文で代用
            #url_list = list(map(partial(self.complement_url,base_url=base_url),urls))
            """
            「001.html」や「../../g1/feb/result/feb2015.html」などパスが揃っていないため
            complement_url関数でパスをそろえる
            """
            for url in urls:
                grades_url.append(self.complement_url(base_url=base_url,url=url))
                print(self.complement_url(base_url=base_url,url=url))
        with open("two_years_ago_urls.txt", "a", encoding = 'UTF-8') as f:
            [f.write(i+"\n") for i in grades_url]
        
    """
    url整形用関数
    base_url(現在クローリングしているurl)をもとに
    ファイル名のみのパスや../やなどの相対パスを補完する
    """
    def complement_url(self,base_url,url):
      hierarchy_cnt = url.count('../') + 1
      url = url.replace('../','',hierarchy_cnt)
      for i in range(hierarchy_cnt):
        base_url = base_url[0:base_url.rindex('/')]
      return base_url + "/" + url
    
