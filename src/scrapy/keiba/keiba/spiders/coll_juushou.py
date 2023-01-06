import scrapy
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
import re
import pandas as pd
import os
import sys
sys.path.append('../../')
from modules.constants import DataFrameCols

class CollJuushouSpider(scrapy.Spider):
  name = 'coll_juushou'
  allowed_domains = ['race.netkeiba.com']
  start_urls = ['https://race.netkeiba.com/top/schedule.html?rf=sidemenu']
  df_cols = DataFrameCols()
  cols = df_cols.juushou_cols()
  df = pd.DataFrame(columns=cols)
  def __init__(self, juushou_year, data_juushou_list, *args, **kwargs):
    super(CollJuushouSpider, self).__init__(*args, **kwargs)
    self.juushou_year = juushou_year
    self.data_juushou_list = data_juushou_list
  def parse(self, response):
    data = {
#      "year": "2017"
      "year": self.juushou_year
    }
    yield FormRequest(
      url = 'https://race.netkeiba.com/top/schedule.html?rf=sidemenu',
      formdata = data,
      callback = self.coll_juushou
      )
  def coll_juushou(self, response):
    juushou_info = response.css("div[class='Table_Container mb00'] tr")
    for juushou in juushou_info:
      juushou_td = juushou.css("td")
      if not juushou_td:
        continue
      juushou_raceid = juushou_td[1].css("a::attr(href)").get(default='')
      juushou_raceid = ''.join(re.findall(r"\d+",juushou_raceid))
      juushou_date = juushou_td[0].css("::text").get(default='')
      juushou_race = juushou_td[1].css("a::text").get(default='')
      juushou_kaku = juushou_td[2].css("::text").get(default='')
      juushou_ba = juushou_td[3].css("::text").get(default='')
      juushou_kyori = juushou_td[4].css("::text").get(default='')
      juushou_jouken = juushou_td[5].css("::text").get(default='')
      juushou_juuryou = juushou_td[6].css("::text").get(default='')
      list_append = [[
        juushou_raceid,
        juushou_date,
        juushou_race,
        juushou_kaku,
        juushou_ba,
        juushou_kyori,
        juushou_jouken,
        juushou_juuryou
      ]]
      df_append = pd.DataFrame(data=list_append,columns=self.cols)
      self.df = pd.concat([self.df, df_append], ignore_index=True, axis=0)
    self.df.to_pickle(self.data_juushou_list)
    print("============================")
    print("■デバッグ")
    print("============================")
    print(self.df)