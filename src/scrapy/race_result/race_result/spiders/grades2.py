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
  name = 'grades2'
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
  
  def haed_add_empty_element(self,element_list):
    element_list.insert(0,'')
    return element_list
  
  def end_add_empty_element(self,element_list):
    element_list.append('')
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
      element_list = self.haed_add_empty_element(element_list)
    if len(element_list) < base_cnt:
      element_list = self.haed_add_empty_element(element_list)
    return element_list

  def align_element(self,element_list,full_cnt):
    print("> ==================================================")
    print("> ■align_element")
    print("> ==================================================")
    print("> full_cnt: " + str(full_cnt))
    print("> element_list_cnt :" + str(len(element_list)))
    print(element_list)
    align_cnt = full_cnt - len(element_list)
    for i in range(align_cnt):
      element_list = self.end_add_empty_element(element_list)
    return element_list

  def parse(self, response):
    sel = Selector(response)
    base_url = str(response.request.url)
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
    #base_cnt = len(response.css("table[class='basic narrow-xy striped'] tbody tr").getall())
    base_cnt = sel.css("table[class='basic narrow-xy striped'] td[class='place']::text").getall()
    base_cnt = len([cnt for cnt in base_cnt if cnt.isdecimal()])
    full_cnt = len(response.css("table[class='basic narrow-xy striped'] tbody tr").getall())
    print("■base_cnt")
    print(base_cnt)

    print("■着順")
    place = sel.css("table[class='basic narrow-xy striped'] td[class='place']::text").getall()
    place = list(map(self.shap_str,place))
    place = self.shap_empty_element(place,base_cnt)
    place = self.align_element(place,full_cnt)
    print(place)
    print("len: " + str(len(place)))
    
    print("■枠")
    waku1 = sel.css("table[class='basic narrow-xy striped'] td[class='waku'] img").xpath('@alt').getall()
    waku1 = [re.sub("\D","",rep) for rep in waku1]
    waku2 = sel.css("table[class='basic narrow-xy striped'] td[class='waku'] img").xpath('@src').getall()
    waku2 = [re.sub("\D","",rep) for rep in waku2]
    print(waku1)
    print("len: " + str(len(waku1)))
    print(waku2)
    print("len: " + str(len(waku2)))
    
    print("■馬番")
    num = sel.css("table[class='basic narrow-xy striped'] td[class='num']::text").getall()
    num = list(map(self.shap_str,num))
    num = self.shap_empty_element(num,base_cnt)
    print(num)
    print("len: " + str(len(num)))

    print("■馬名")
    horse = sel.css("table[class='basic narrow-xy striped'] td[class='horse']::text").getall()
    horse = list(map(self.shap_str,horse))
    horse = self.del_empty_element(horse) if len(horse) > base_cnt else horse
    horse = self.shap_empty_element(horse,base_cnt)
    print(horse)
    print("len: " + str(len(horse)))
    
    print("■性齢")
    age = sel.css("table[class='basic narrow-xy striped'] td[class='age']::text").getall()
    age = list(map(self.shap_str,age))
    age = self.shap_empty_element(age,base_cnt)
    print(age)
    print("len: " + str(len(age)))
    
    print("■負担重量")
    weight = sel.css("table[class='basic narrow-xy striped'] td[class='weight']::text").getall()
    weight = list(map(self.shap_str,weight))
    weight = self.shap_empty_element(weight,base_cnt)
    print(weight)
    print("len: " + str(len(weight)))

    print("■騎手名")
    jockey = sel.css("table[class='basic narrow-xy striped'] td[class='jockey']::text").getall()
    jockey = list(map(self.shap_str,jockey))
    jockey = self.shap_empty_element(jockey,base_cnt)
    print(jockey)
    print("len: " + str(len(jockey)))
    
    print("■タイム")
    time = sel.css("table[class='basic narrow-xy striped'] td[class='time']::text").getall()
    time = list(map(self.shap_str,time))
    time = self.shap_empty_element(time,base_cnt)
    time = self.align_element(time,full_cnt)
    print(time)
    print("len: " + str(len(time)))
    
    print("■着差")
    margin = sel.css("table[class='basic narrow-xy striped'] td[class='margin']::text").getall()
    margin = list(map(self.shap_str,margin))
    margin = self.shap_empty_element(margin,base_cnt)
    print(margin)
    print("len: " + str(len(margin)))
    
    print("■コーナー週過順位")
    corner = []
    for ul in sel.css("table[class='basic narrow-xy striped'] td[class='corner'] ul"):
      ul_data = ul.css("li::text").getall()
      corner.append(list(map(self.shap_str,ul_data)))
    print(corner)
    print("len: " + str(len(corner)))
    
    print("■推定上がり")
    f_time = sel.css("table[class='basic narrow-xy striped'] td[class='f_time']::text").getall()
    f_time = list(map(self.shap_str,f_time))
    f_time = self.shap_empty_element(f_time,base_cnt)
    print(f_time)
    print("len: " + str(len(f_time)))

    print("■馬体重(増減)")
    h_weight = sel.css("table[class='basic narrow-xy striped'] td[class='h_weight']::text").getall()
    iod_weight = sel.css("table[class='basic narrow-xy striped'] td[class='h_weight'] span::text").getall()
    h_weight = list(map(self.shap_str,h_weight))
    h_weight = self.shap_empty_element(h_weight,base_cnt)
    iod_weight = list(map(self.shap_str,iod_weight))
    iod_weight = self.shap_empty_element(iod_weight,base_cnt)
    print(h_weight)
    print("len: " + str(len(h_weight)))
    print(iod_weight)
    print("len: " + str(len(iod_weight)))

    print("■調教師名")
    trainer = sel.css("table[class='basic narrow-xy striped'] td[class='trainer']::text").getall()
    trainer = list(map(self.shap_str,trainer))
    trainer = self.shap_empty_element(trainer,base_cnt)
    print(trainer)
    print("len: " + str(len(trainer)))

    print("■単勝人気")
    pop = sel.css("table[class='basic narrow-xy striped'] td[class='pop']::text").getall()
    pop = list(map(self.shap_str,pop))
    pop = self.shap_empty_element(pop,base_cnt)
    print(pop)
    print("len: " + str(len(pop)))
    df1 = pd.DataFrame(
      data={'着順': place,
            '枠': waku1,
            '馬番': num,
            '馬名': horse,
            '性齢': age,
            '負担重量': weight,
            '騎手名': jockey,
            'タイム': time,
            '着差': margin,
            'コーナー週過順位': weight,
            '推定上がり': f_time,
            '馬体重': h_weight,
            '馬体重(増減)': iod_weight,
            '調教師名': trainer,
            '単勝人気': pop}
    )
    
    if len(race_title) != 0:
      print("■pickleタイトル")
      print(race_title)
      df1.to_pickle('../pickle/' + race_title)
    
