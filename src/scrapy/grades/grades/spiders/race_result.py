import os
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from grades.items import GradesItem
import pandas as pd
import numpy as np
import re

class GradesSpider(scrapy.Spider):
  name = 'race_result'
  allowed_domains = ['www.jra.go.jp']
  #start_urls = np.ravel(pd.read_csv('../grades_urls.csv',header=1).values.tolist())
  #print(start_urls)
  
  """
  start_urlsに複数のurlを指定するため、start_requests関数を定義
  """
  def start_requests(self):
    for url in np.ravel(pd.read_csv('../tmp/grades_urls.csv',header=0).values.tolist()):
      yield scrapy.Request(url)
  
  def shap_str(self,str_data):
    shap_symbol = str.maketrans('／（）１２３４５６７８９０','/()1234567890')
    str_data = str_data.translate(shap_symbol)
    str_data = re.sub("\n|  +|\(|\)","",str_data)
    str_data = str_data.replace(u'\xa0', u'')
    return str_data
  
  def one_line_list(self,join_list):
    join_list = ''.join(join_list)
    return join_list
  
  def err_msg(self):
    print("スクレイピング不可")

  #def del_empty_element(self,element_list):
  #  element_list = [element for element in element_list if element != '']
  #  return element_list
  
  #def haed_add_empty_element(self,element_list):
  #  element_list.insert(0,'')
  #  return element_list
  
  #def end_add_empty_element(self,element_list):
  #  element_list.append('')
  #  return element_list
  
  #def shap_empty_element(self,element_list,base_cnt):
  #  print("> ==================================================")
  #  print("> ■shap_empty_element")
  #  print("> ==================================================")
  #  print("> base_cnt: " + str(base_cnt))
  #  print("> element_list_cnt :" + str(len(element_list)))
  #  print(element_list)
  #  if len(element_list) > base_cnt:
  #    element_list = self.del_empty_element(element_list)
  #  elif len(element_list) < base_cnt:
  #    element_list = self.haed_add_empty_element(element_list)
  #  if len(element_list) < base_cnt:
  #    element_list = self.haed_add_empty_element(element_list)
  #  return element_list

  #def align_element(self,element_list,full_cnt):
  #  print("> ==================================================")
  #  print("> ■align_element")
  #  print("> ==================================================")
  #  print("> full_cnt: " + str(full_cnt))
  #  print("> element_list_cnt :" + str(len(element_list)))
  #  print(element_list)
  #  align_cnt = full_cnt - len(element_list)
  #  for i in range(align_cnt):
  #    element_list = self.end_add_empty_element(element_list)
  #  return element_list

  def parse(self, response):
    sel = Selector(response)
    base_url = str(response.request.url)
    print("==================================================")
    print("■URL")
    print("==================================================")
    print(base_url)

    race_header = sel.css("div[class='race_header']")
    if not len(race_header) > 0:
      print("スクレイピング不可")
      return

    print("==================================================")
    print("■レースヘッダー")
    print("==================================================")
    for rh in race_header:
      race_title = rh.css("div[class='txt'] span[class='race_name']::text").getall()
      race_title = list(map(self.shap_str,race_title))
      race_title = self.one_line_list(race_title)
      print(race_title)
      race_date = rh.css("div[class='cell date']::text").getall()
      race_date = list(map(self.shap_str,race_date))
      race_date = self.one_line_list(race_date)
      race_date = re.sub(" .*","",race_date)
      print(race_date)
      race_category = rh.css("div[class='type'] div[class='cell category']::text").getall()
      race_category = list(map(self.shap_str,race_category))
      race_category = self.one_line_list(race_category)
      print(race_category)
      race_class = rh.css("div[class='type'] div[class='cell class']::text").getall()
      race_class = list(map(self.shap_str,race_class))
      race_class = self.one_line_list(race_class)
      print(race_class)
      race_rule = rh.css("div[class='type'] div[class='cell rule']::text").getall()
      race_rule = list(map(self.shap_str,race_rule))
      race_rule = self.one_line_list(race_rule)
      print(race_rule)
      race_weight = rh.css("div[class='type'] div[class='cell weight']::text").getall()
      race_weight = list(map(self.shap_str,race_weight))
      race_weight = self.one_line_list(race_weight)
      print(race_weight)
      course_distance = rh.css("div[class='type'] div[class='cell course']::text").getall()
      course_unit = rh.css("div[class='type'] div[class='cell course'] span[class='unit']::text").getall()
      course_detail = rh.css("div[class='type'] div[class='cell course'] span[class='detail']::text").getall()
      course_distance = list(map(self.shap_str,course_distance))
      course_unit = list(map(self.shap_str,course_unit))
      course_detail = list(map(self.shap_str,course_detail))
      race_course = course_distance + course_unit + course_detail
      race_course = self.one_line_list(race_course)

      print(race_course)
      pickle_name = race_date + race_category + race_class + race_rule + race_course
      pickle_name = list(map(self.shap_str,pickle_name))
      pickle_name = self.one_line_list(pickle_name)
      pickle_name = re.sub(" ","",pickle_name)
    
    print("==================================================")
    print("■レース名")
    print("==================================================")
    print(pickle_name)

    race_data = sel.css("table[class='basic narrow-xy striped'] tbody tr")
    if not len(race_data) > 0:
      print("レース詳細情報のスクレイピング不可")
      return
    
    print("==================================================")
    print("■レース詳細情報")
    print("==================================================")

    """
    tableのtdを二次元配列で取得
    """
    place_list = []
    waku1_list = []
    waku2_list = []
    num_list = []
    horse_list = []
    age_list = []
    weight_list = []
    jockey_list = []
    time_list = []
    margin_list = []
    corner_list = []
    f_time_list = []
    h_weight_list = []
    iod_weight_list = []
    trainer_list = []
    pop_list = []
    for rd in race_data:
      #base_cnt = len(response.css("table[class='basic narrow-xy striped'] tbody tr").getall())
      #base_cnt = tr.css("table[class='basic narrow-xy striped'] td[class='place']::text").getall()
      #base_cnt = len([cnt for cnt in base_cnt if cnt.isdecimal()])
      #full_cnt = len(response.css("table[class='basic narrow-xy striped'] tbody tr").getall())
      #print("■base_cnt")
      #print(base_cnt)

      """
      ■着順
      """
      place = rd.css("td[class='place']::text").getall()
      place = list(map(self.shap_str,place))
      place_list.append(self.one_line_list(place))
      #place = self.shap_empty_element(place,base_cnt)
      #place = self.align_element(place,full_cnt)

      """
      ■枠
      """
      waku1 = rd.css("td[class='waku'] img").xpath('@alt').getall()
      waku1 = [re.sub("\D","",rep) for rep in waku1]
      waku2 = rd.css("td[class='waku'] img").xpath('@src').getall()
      waku2 = [re.sub("\D","",rep) for rep in waku2]
      waku1_list.append(self.one_line_list(waku1))
      waku2_list.append(self.one_line_list(waku2))
      
      """
      ■馬番
      """
      num = rd.css("td[class='num']::text").getall()
      num = list(map(self.shap_str,num))
      num_list.append(self.one_line_list(num))
      #num = self.shap_empty_element(num,base_cnt)
      
      """
      ■馬名
      """
      horse = rd.css("td[class='horse']::text").getall()
      horse = list(map(self.shap_str,horse))
      horse_list.append(self.one_line_list(horse))
      #horse = self.del_empty_element(horse) if len(horse) > base_cnt else horse
      #horse = self.shap_empty_element(horse,base_cnt)
      
      """
      ■性齢
      """
      age = rd.css("td[class='age']::text").getall()
      age = list(map(self.shap_str,age))
      age_list.append(self.one_line_list(age))
      #age = self.shap_empty_element(age,base_cnt)
      
      """
      ■負担重量
      """
      weight = rd.css("td[class='weight']::text").getall()
      weight = list(map(self.shap_str,weight))
      weight_list.append(self.one_line_list(weight))
      #weight = self.shap_empty_element(weight,base_cnt)
      
      """
      ■騎手名
      """
      jockey = rd.css("td[class='jockey']::text").getall()
      jockey = list(map(self.shap_str,jockey))
      jockey_list.append(self.one_line_list(jockey))
      #jockey = self.shap_empty_element(jockey,base_cnt)
      
      """
      ■タイム
      """
      time = rd.css("td[class='time']::text").getall()
      time = list(map(self.shap_str,time))
      time_list.append(self.one_line_list(time))
      #time = self.shap_empty_element(time,base_cnt)
      #time = self.align_element(time,full_cnt)
      
      """
      ■着差
      """
      margin = rd.css("td[class='margin']::text").getall()
      margin = list(map(self.shap_str,margin))
      margin_list.append(self.one_line_list(margin))
      #margin = self.shap_empty_element(margin,base_cnt)
      
      """
      ■コーナー週過順位
      """
      for ul in rd.css("td[class='corner'] ul"):
        ul_data = ul.css("li::text").getall()
        #ul_data = '-'.join(ul_data)
        ul_data = list(map(self.shap_str,ul_data))
        ul_data = '-'.join(ul_data) if self.one_line_list(ul_data) else self.one_line_list(ul_data)
        corner_list.append(ul_data)
      #corner_list.append(corner)

      """
      ■推定上がり
      """
      f_time = rd.css("td[class='f_time']::text").getall()
      f_time = list(map(self.shap_str,f_time))
      f_time_list.append(self.one_line_list(f_time))
      #f_time = self.shap_empty_element(f_time,base_cnt)
      
      """
      ■馬体重(増減)
      """
      h_weight = rd.css("td[class='h_weight']::text").getall()
      iod_weight = rd.css("td[class='h_weight'] span::text").getall()
      h_weight = list(map(self.shap_str,h_weight))
      #h_weight = self.shap_empty_element(h_weight,base_cnt)
      iod_weight = list(map(self.shap_str,iod_weight))
      #iod_weight = self.shap_empty_element(iod_weight,base_cnt)
      h_weight_list.append(self.one_line_list(h_weight))
      iod_weight_list.append(self.one_line_list(iod_weight))
      
      """
      ■調教師名
      """
      trainer = rd.css("td[class='trainer']::text").getall()
      trainer = list(map(self.shap_str,trainer))
      trainer_list.append(self.one_line_list(trainer))
      #trainer = self.shap_empty_element(trainer,base_cnt)
      
      """
      ■単勝人気
      """
      pop = rd.css("td[class='pop']::text").getall()
      pop = list(map(self.shap_str,pop))
      pop_list.append(self.one_line_list(pop))
      #pop = self.shap_empty_element(pop,base_cnt)
    print("■着順")
    print(place_list)
    print("len: " + str(len(place_list)))
    print("■枠")
    print(waku1)
    print("len: " + str(len(waku1_list)))
    print(waku2)
    print("len: " + str(len(waku2_list)))
    print("■馬番")
    print(num_list)
    print("len: " + str(len(num_list)))
    print("■馬名")
    print(horse_list)
    print("len: " + str(len(horse_list)))
    print("■性齢")
    print(age_list)
    print("len: " + str(len(age_list)))
    print("■負担重量")
    print(weight_list)
    print("len: " + str(len(weight_list)))
    print("■騎手名")
    print(jockey_list)
    print("len: " + str(len(jockey_list)))
    print("■タイム")
    print(time_list)
    print("len: " + str(len(time_list)))
    print("■着差")
    print(margin_list)
    print("len: " + str(len(margin_list)))
    print("■コーナー週過順位")
    print(corner_list)
    print("len: " + str(len(corner_list)))
    print("■推定上がり")
    print(f_time_list)
    print("len: " + str(len(f_time_list)))
    print("■馬体重(増減)")
    print(h_weight_list)
    print("len: " + str(len(h_weight_list)))
    print("■iod_weight_list")
    print(iod_weight_list)
    print("len: " + str(len(iod_weight_list)))
    print("■調教師名")
    print(trainer_list)
    print("len: " + str(len(trainer_list)))
    print("■単勝人気")
    print(pop_list)
    print("len: " + str(len(pop_list)))

    df1 = pd.DataFrame(
      data={'レース日': "",
            'レースタイトル': "",
            'レースカテゴリ': "",
            'レースクラス': "",
            'レースルール': "",
            'レース重量': "",
            'レースコース': "",
            '着順': place_list,
            '枠': waku1_list,
            '馬番': num_list,
            '馬名': horse_list,
            '性齢': age_list,
            '負担重量': weight_list,
            '騎手名': jockey_list,
            'タイム': time_list,
            '着差': margin_list,
            'コーナー週過順位': corner_list,
            '推定上がり': f_time_list,
            '馬体重': h_weight_list,
            '馬体重(増減)': iod_weight_list,
            '調教師名': trainer_list,
            '単勝人気': pop_list}
      )
    print(df1)
    df1["レース日"] = race_date
    df1["レースタイトル"] = race_title
    df1["レースカテゴリ"] = race_category
    df1["レースクラス"] = race_class
    df1["レースルール"] = race_rule
    df1["レース重量"] = race_weight
    df1["レースコース"] = race_course
    if len(pickle_name) != 0:
      print("■pickleタイトル")
      print(pickle_name)
      df1.to_pickle('../pickle/' + pickle_name)
      #df1.to_csv('../csv1/' + race_title + '.csv')
      