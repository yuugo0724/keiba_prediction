import os
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from race_result.items import RaceResultItem
import pandas as pd
import numpy as np
import re

class GradesSpider(scrapy.Spider):
  name = 'grades1'
  allowed_domains = ['www.jra.go.jp']
  #start_urls = np.ravel(pd.read_csv('../grades_urls.csv',header=1).values.tolist())
  print(os.getcwd())
  #print(start_urls)
  
  """
  start_urlsに複数のurlを指定するため、start_requests関数を定義
  """
  def start_requests(self):
    for url in np.ravel(pd.read_csv('../grades_urls.csv',header=0).values.tolist()):
      yield scrapy.Request(url)
  
  def shap_str(self,str_data):
    shap_symbol = str.maketrans('／（）１２３４５６７８９０','/()1234567890')
    str_data = re.sub("\n|  +|\(|\)","",str_data).translate(shap_symbol)
    return str_data
  
  def one_line_list(self,join_list):
    join_list = ''.join(join_list)
    return join_list

  def del_empty_element(self,element_list):
    element_list = [element for element in element_list if element != '']
    return element_list
  
  def add_empty_element(self,element_list):
    element_list.insert(0,'')
    return element_list
  
  def shap_empty_element(self,element_list,base_cnt):
    print("> ==================================================")
    print("> ■shap_empty_element")
    print("> ==================================================")
    print("> base_cnt: " + str(base_cnt))
    print("> element_list_cnt :" + str(len(element_list)))
    print(element_list)
    if len(element_list) > base_cnt:
      element_list = self.del_empty_element(element_list)
    elif len(element_list) < base_cnt:
      element_list = self.add_empty_element(element_list)
    if len(element_list) < base_cnt:
      element_list = self.add_empty_element(element_list)
    return element_list


  def parse(self, response):
    sel = Selector(response)
    base_url = str(response.request.url)
    base_cnt = len(response.css("table[class='basic narrow-xy striped'] tbody tr").getall())
    print("==================================================")
    print("■URL")
    print("==================================================")
    print(base_url)

    print("==================================================")
    print("■レースヘッダー")
    print("==================================================")
    race_date = sel.css("div[class='race_header'] div[class='cell date']::text").getall()
    race_date = list(map(self.shap_str,race_date))
    race_date = self.one_line_list(race_date)
    print(race_date)
    race_category = sel.css("div[class='race_header'] div[class='type'] div[class='cell category']::text").getall()
    race_category = list(map(self.shap_str,race_category))
    race_category = self.one_line_list(race_category)
    print(race_category)
    race_class = sel.css("div[class='race_header'] div[class='type'] div[class='cell class']::text").getall()
    race_class = list(map(self.shap_str,race_class))
    race_class = self.one_line_list(race_class)
    print(race_class)
    race_rule = sel.css("div[class='race_header'] div[class='type'] div[class='cell rule']::text").getall()
    race_rule = list(map(self.shap_str,race_rule))
    race_rule = self.one_line_list(race_rule)
    print(race_rule)
    race_weight = sel.css("div[class='race_header'] div[class='type'] div[class='cell weight']::text").getall()
    race_weight = list(map(self.shap_str,race_weight))
    race_weight = self.one_line_list(race_weight)
    print(race_weight)
    race_course = sel.css("div[class='race_header'] div[class='type'] div[class='cell course'] ::text").getall()
    race_course = list(map(self.shap_str,race_course))
    race_course = self.one_line_list(race_course)
    print(race_course)
    race_title = race_date + race_category + race_class + race_rule + race_course
    race_title = list(map(self.shap_str,race_title))
    race_title = self.one_line_list(race_title)
    race_title = re.sub(" ","",race_title)
    print("==================================================")
    print("■レースタイトル")
    print("==================================================")
    print(race_title)

    print("==================================================")
    print("■レース詳細情報")
    print("==================================================")

    grades_list = sel.css("table[class='basic narrow-xy striped'] tr>*::text").getall()
    grades_list = np.array(grades_list).reshape(-1, 3).tolist()
    print(grades_list)
