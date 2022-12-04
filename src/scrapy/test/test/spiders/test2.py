import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import pandas as pd
import numpy as np
import re

class Test1Spider(scrapy.Spider):
  name = 'test1'
  allowed_domains = ['www.jra.go.jp']
    
  def start_requests(self):
    for url in np.ravel(pd.read_csv('../grades_urls.csv',header=0).values.tolist()):
      yield scrapy.Request(url)
  
  def shap_str(self,str_data):
    shap_symbol = str.maketrans('／（）１２３４５６７８９０','/()1234567890')
    str_data = re.sub("\n|  +|\(|\)","",str_data).translate(shap_symbol)
    return str_data
  
  def parse(self, response):
    sel = Selector(response)
    for tr in sel.css("table[class='basic narrow-xy striped'] tbody tr"):
      tr_data = tr.css("td::text").getall()
      waku = tr.css("td[class='waku'] img").xpath('@alt').get(default='')
      waku = re.sub("\D","",str(waku))
      tr_data.insert(1,waku)
      tr_data = list(map(self.shap_str,tr_data))
      print(tr_data)
      