import scrapy
from scrapy.selector import Selector
import pandas as pd
import os
import re

class CollHorseGradesSpider(scrapy.Spider):
  name = 'coll_horse_grades'
  allowed_domains = ['db.netkeiba.com']
  #start_urls = ["https://db.netkeiba.com/race/199201010701/"]
  def __init__(self, horse_id, data_master_horse_grades, *args, **kwargs):
    super(CollHorseGradesSpider, self).__init__(*args, **kwargs)
    self.start_urls = ['https://db.netkeiba.com/horse/result/' + horse_id]
    self.horse_id = horse_id
    self.data_master_horse_grades = data_master_horse_grades

  def map_split_str(self, str_data):
    str_data_list = re.findall(r'\w+', str_data)
    return str_data_list
  
  def parse(self, response):
    sel = Selector(response)
    cols = [
      "日付",
      "開催",
      "天気",
      "R",
      "レース名",
      "レース_ID",
      #"映像",
      "頭数",
      "枠番",
      "馬番",
      "オッズ",
      "人気",
      "着順",
      "騎手",
      "騎手_ID",
      "斥量",
      "距離",
      "レースタイプ",
      "馬場",
      "タイム",
      "着差",
      "通過",
      "ペース",
      "上り",
      "馬体重",
      "馬体重増減",
      "勝ち馬(2着馬)",
      "賞金"
      ]
    df = pd.DataFrame(columns=cols)
    horse_data = sel.css("div[class='db_main_deta mb30']>table tr")
    # レースがない場合、処理を終了
    if not horse_data:
      return
    for result in horse_data:
      result_td = result.css("td")
      if not result_td:
        continue
      date = result_td[0].css("a::text").get()
      hold = result_td[1].css("a::text").get()
      weather = result_td[2].css("::text").get()
      aru = result_td[3].css("::text").get()
      race_name = result_td[4].css("a::text").get()
      race_name_info = result_td[4].css("a::attr(href)").get()
      race_id_list = race_name_info.split('/')
      race_id = race_id_list[2]
      movie = result_td[5]
      horse_num = result_td[6].css("::text").get()
      waku_ban = result_td[7].css("::text").get()
      baban = result_td[8].css("::text").get()
      odds = result_td[9].css("::text").get()
      rank = result_td[10].css("::text").get()
      chakujun = result_td[11].css("::text").get()
      jockey = result_td[12].css("a::text").get()
      jockey_info = result_td[12].css("a::attr(href)").get()
      jockey_list = jockey_info.split('/')
      jockey_id = jockey_list[4]
      load = result_td[13].css("::text").get()
      meters_info = result_td[14].css("::text").get()
      meters = re.sub(r'\D',"",meters_info)
      race_type = re.sub(r'\d+',"",meters_info)
      baba = result_td[15].css("::text").get()
      time = result_td[17].css("::text").get()
      chakusa = result_td[18].css("::text").get()
      tuuka = result_td[20].css("::text").get()
      pace = result_td[21].css("::text").get()
      nobori = result_td[22].css("::text").get()
      weight_info = result_td[23].css("::text").get()
      weight_info_list = re.findall(r'\d+',weight_info)
      weight = weight_info_list[0]
      inc_dec = ''.join(re.findall(r'\+|\-',weight_info))
      weight_inc_dec = inc_dec + weight_info_list[1]
      katiuma = result_td[26].css("a::text").get()
      prize = result_td[27].css("::text").get()
      list_append = [[
        date,
        hold,
        weather,
        aru,
        race_name,
        race_id,
        #movie,
        horse_num,
        waku_ban,
        baban,
        odds,
        rank,
        chakujun,
        jockey,
        jockey_id,
        load,
        meters,
        race_type,
        baba,
        time,
        chakusa,
        tuuka,
        pace,
        nobori,
        weight,
        weight_inc_dec,
        katiuma,
        prize
        ]]
      print(list_append)
      df_append = pd.DataFrame(data=list_append,columns=cols)
      df = pd.concat([df, df_append], ignore_index=True, axis=0)
    df.to_pickle(os.path.join(self.data_master_horse_grades,self.horse_id))
    print("============================")
    print("■デバッグ")
    print("============================")
    print(df)
