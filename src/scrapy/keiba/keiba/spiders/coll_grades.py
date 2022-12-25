import scrapy
from scrapy.selector import Selector
import pandas as pd
import os
import re
import sys
sys.path.append('../../')
from modules.constants import DataFrameCols

class CollGradesSpider(scrapy.Spider):
  name = 'coll_grades'
  allowed_domains = ['db.netkeiba.com']
  #start_urls = ["https://db.netkeiba.com/race/199201010701/"]
  df_cols = DataFrameCols()
  scrapy_grades_cols = df_cols.scrapy_grades_cols()
  def __init__(self, url, race_id, date_dir, *args, **kwargs):
    super(CollGradesSpider, self).__init__(*args, **kwargs)
    self.start_urls = [url]
    self.race_id = race_id
    self.date_dir = date_dir

  def map_split_str(self, str_data):
    str_data_list = re.findall(r'\w+', str_data)
    return str_data_list
  
  def parse(self, response):
    sel = Selector(response)
    cols = self.scrapy_grades_cols
    df = pd.DataFrame(columns=cols)
    race_header = sel.css("div[class='netkeiba_toprace_block'] div[class='race_head_inner'] diary_snap dl[class='racedata fc']")
    race_name = sel.css("dd>h1::text").get()
    race_info = sel.css("dd p diary_snap_cut span::text").get()
    race_info = race_info.replace(u'\xa0', u' ')
#    race_info = re.sub(" ","",race_info)
#    race_info = re.findall(r'\w+', race_info)
#    race_meters = re.sub("\D","",race_info[0])
#    race_around = re.findall('右|左|障', race_info[0])
#    if not race_around:
#      race_around = ['']
#    #race_type = race_info[0]
#    #race_weather = race_info[2]
#    race_type = re.findall('芝|ダート|ダ|障', race_info[0])
#    race_status = race_info[4]
    result_data = sel.css("table[summary='レース結果'] tr")
    # レースがない場合、処理を終了
    if not result_data:
      return
    for result in result_data:
      result_td = result.css("td")
      if not result_td:
        continue
      rank = result_td[0].css("::text").get()
      waku_num = result_td[1].css("span::text").get()
      horse_num = result_td[2].css("::text").get()
      horse_name = result_td[3].css("a::text").get()
      horse_id_info = result_td[3].css("a::attr(href)").get()
      horse_id = ''.join(re.findall(r'\d+',horse_id_info))
      age = result_td[4].css("::text").get()
      load = result_td[5].css("::text").get()
      jockey = result_td[6].css("a::text").get()
      jockey_id_info = result_td[6].css("a::attr(href)").get()
      jockey_id = ''.join(re.findall(r'\d+',jockey_id_info))
      time = result_td[7].css("::text").get()
      chakusa = result_td[8].css("::text").get()
      keika = result_td[10].css("::text").get()
      nobori = result_td[11].css("span::text").get()
      odds = result_td[12].css("::text").get()
      pop = result_td[13].css("span::text").get()
      weight_info = result_td[14].css("::text").get()
      weight_info_list = re.findall(r'\d+',weight_info)
      weight = weight_info_list[0]
      inc_dec = ''.join(re.findall(r'\+|\-',weight_info))
      weight_inc_dec = inc_dec + weight_info_list[1]
      trainer = result_td[18].css("a::text").get()
      trainer_id_info = result_td[18].css("a::attr(href)").get()
      trainer_id = ''.join(re.findall(r'\d+',trainer_id_info))
      horse_owner = result_td[19].css("a::text").get()
      prize = result_td[20].css("::text").get()
      list_append = [[
        self.race_id,
        race_name,
        race_info,
#        race_meters,
#        race_around[0],
        #race_weather,
#        race_type,
#        race_status,
        rank,
        waku_num,
        horse_num,
        horse_name,
        age,
        load,
        jockey,
        time,
        odds,
        pop,
        weight,
        weight_inc_dec,
        trainer,
        horse_id,
        jockey_id,
        trainer_id
        ]]
      df_append = pd.DataFrame(data=list_append,columns=cols)
      df = pd.concat([df, df_append], ignore_index=True, axis=0)
    df.to_pickle(os.path.join(self.date_dir,self.race_id))
    print("============================")
    print("■デバッグ")
    print("============================")
    print(df)
