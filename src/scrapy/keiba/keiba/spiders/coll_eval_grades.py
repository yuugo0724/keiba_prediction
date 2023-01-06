import scrapy
from scrapy.selector import Selector
import pandas as pd
import os
import re
import sys
sys.path.append('../../')
from modules.constants import DataFrameCols

class CollPredGradesSpider(scrapy.Spider):
  name = 'coll_eval_grades'
  allowed_domains = ['db.netkeiba.com']
  #start_urls = ["https://db.netkeiba.com/race/199201010701/"]
  df_cols = DataFrameCols()
  pred_data_cols = df_cols.pred_data_cols()
  def __init__(self, url, pred_dir, *args, **kwargs):
    super(CollPredGradesSpider, self).__init__(*args, **kwargs)
    self.start_urls = [url]
    self.pred_dir = pred_dir
    race_id_info = re.findall(r'\d+',url)
    self.race_id = ''.join(race_id_info)

  def map_split_str(self, str_data):
    str_data_list = re.findall(r'\w+', str_data)
    return str_data_list
  
  def parse(self, response):
    sel = Selector(response)
    cols = self.pred_data_cols
    df = pd.DataFrame(columns=cols)
    race_header = sel.css("div[class='RaceList_NameBox']")
    race_name = race_header.css("div[class='RaceName']::text").get(default='')
    race_name = re.sub(r'\n','',race_name)
    race_info = race_header.css("div[class='RaceData01']::text, div[class='RaceData01'] span::text").getall()
    race_info = [re.sub(r'\n','',info) for info in race_info]
    race_info = ''.join(race_info)
    race_info = race_info.replace(u'\xa0', u' ')
    #race_info_detail = race_info.css("div[class='RaceData01'] span::text").get()
    #race_meters = re.sub("\D","",race_info_detail)
    #race_type = re.findall('芝|ダ|障', race_info_detail)
    #race_type = race_type[0]
    #race_around = race_info.css("div[class='RaceData01']::text").getall()
    #race_around = re.findall('右|左|障', race_around[1])
    #if not race_around:
    #  race_around = ['']
    #race_type = race_info[0]
    #race_weather = race_info[2]
    #race_type = race_info[3]
    #race_status = race_info[4]
    result_data = sel.css("div[class='ResultTableWrap'] tr")
    # レースがない場合、処理を終了
    if not result_data:
      return
    for result in result_data:
      result_td = result.css("td")
      if not result_td:
        continue
      #rank = result_td[0].css("::text").get()
      waku_num = result_td[1].css("div::text").get(default=0)
      horse_num = result_td[2].css("div::text").get(default=0)
      horse_name = result_td[3].css("a::text").get(default='')
      horse_id_info = result_td[3].css("a::attr(href)").get(default='')
      horse_id = ''.join(re.findall(r'\d+',horse_id_info))
      sexual_age = result_td[4].css("span::text").get(default='')
      sexual_age = re.sub(r"\n","",sexual_age)
      load = result_td[5].css("span::text").get(default=0)
      jockey = result_td[6].css("a::text, ::text").getall()
      jockey = ''.join(jockey)
      jockey = re.sub(r"\n","",jockey)
      jockey_id_info = result_td[6].css("a::attr(href)").get(default='')
      jockey_id = ''.join(re.findall(r'\d+',jockey_id_info))
      trainer = result_td[13].css("a::text").get(default='')
      trainer_id_info = result_td[13].css("a::attr(href)").get(default='')
      trainer_id = ''.join(re.findall(r'\d+',trainer_id_info))
      #time = result_td[7].css("::text").get()
      #chakusa = result_td[8].css("::text").get()
      #keika = result_td[10].css("::text").get()
      #nobori = result_td[11].css("span::text").get()
      #odds = result_td[12].css("::text").get()
      #pop = result_td[13].css("span::text").get()
      weight = result_td[14].css("::text").get(default='0')
      weight = re.sub(r'\n','',weight)
      weight_inc_dec = result_td[14].css("small::text").get(default='0')
      weight_inc_dec = re.sub('\(|\)','',weight_inc_dec)
#      weight_info = result_td[8].css("::text").get()
#      weight_info_list = re.findall(r'\d+',weight_info)
#      print("■weight_info_list")
#      print(weight_info_list)
#      if not weight_info_list:
#        weight = None
#        inc_dec = None
#        weight_inc_dec = None
#      else:
#        weight = weight_info_list[0]
#        inc_dec = ''.join(re.findall(r'\+|\-',weight_info))
#        weight_inc_dec = inc_dec + weight_info_list[1]
      #trainer_id_info = result_td[18].css("a::attr(href)").get()
      #trainer_id = ''.join(re.findall(r'\d+',trainer_id_info))
      #horse_owner = result_td[19].css("a::text").get()
      #prize = result_td[20].css("::text").get()
      list_append = [[
        self.race_id,
        race_name,
        race_info,
#        race_meters,
#        race_around[0],
        #race_weather,
#        race_type,
        #race_status,
        #rank,
        waku_num,
        horse_num,
        horse_name,
        sexual_age,
        load,
        jockey,
        #time,
        #odds,
        #pop,
        weight,
        weight_inc_dec,
        trainer,
        horse_id,
        jockey_id,
        trainer_id
        ]]
      df_append = pd.DataFrame(data=list_append,columns=cols)
      df = pd.concat([df, df_append], ignore_index=True, axis=0)
    df.to_pickle(os.path.join(self.pred_dir,"pred_race_grades"))
    print("============================")
    print("■デバッグ")
    print("============================")
    print(df)
