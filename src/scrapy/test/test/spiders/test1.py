import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import pandas as pd
import numpy as np
import re

class Test1Spider(scrapy.Spider):
  name = 'test2'
  allowed_domains = ['www.jra.go.jp']
    
  def start_requests(self):
    for url in np.ravel(pd.read_csv('../grades_urls.csv',header=0).values.tolist()):
      yield scrapy.Request(url)
  
  def shap_str(self,str_data):
    shap_symbol = str.maketrans('／（）１２３４５６７８９０','/()1234567890')
    str_data = str_data.translate(shap_symbol)
    str_data = re.sub("\n|  +|\(|\)","",str(str_data))
    return str_data
  
  def parse(self, response):
    sel = Selector(response)
    for tr in sel.css("table[class='basic narrow-xy striped'] tr"):
      tr_data = tr.css("td::text").getall()
      print(tr_data)
      place = tr.css("td[class='place']::text").getall()
      print("place")
      print(place)
      waku = self.shap_str(tr.css("td[class='waku'] img").xpath('@alt').getall())
      waku = re.sub("\D","",str(waku))
      print("waku")
      print(waku)
      num = self.shap_str(tr.css("td[class='num']::text").getall())
      print("num")
      print(num)
      horse = self.shap_str(tr.css("td[class='horse']::text").getall())
      print("horse")
      print(horse)
      age = self.shap_str(tr.css("td[class='age']::text").getall())
      print("age")
      print(age)
      weight = self.shap_str(tr.css("td[class='weight']::text").getall())
      print("weight")
      print(weight)
      jockey = self.shap_str(tr.css("td[class='jockey']::text").getall())
      print("jockey")
      print(jockey)
      time = self.shap_str(tr.css("td[class='time']::text").getall())
      print("time")
      print(time)
      margin = self.shap_str(tr.css("td[class='margin']::text").getall())
      print("margin")
      print(margin)
      corner = self.shap_str(tr.css("td[class='corner']::text").getall())
      print("corner")
      print(corner)
      f_time = self.shap_str(tr.css("td[class='f_time']::text").getall())
      print("f_time")
      print(f_time)
      h_weight = self.shap_str(tr.css("td[class='h_weight']::text").getall())
      print("h_weight")
      print(h_weight)
      iod_weight = self.shap_str(tr.css("td[class='iod_weight']::text").getall())
      print("iod_weight")
      print(iod_weight)
      trainer = self.shap_str(tr.css("td[class='trainer']::text").getall())
      print("trainer")
      print(trainer)
      pop = self.shap_str(tr.css("td[class='pop']::text").getall())
      print("pop")
      print(pop)
      