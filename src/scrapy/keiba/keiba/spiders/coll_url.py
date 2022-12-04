import scrapy
from scrapy.selector import Selector
import pandas as pd
import os

class CollUrlSpider(scrapy.Spider):
  name = 'coll_url'
  allowed_domains = ['db.netkeiba.com']
  #start_urls = ["https://db.netkeiba.com/?pid=race_top"]
  base_list_url = 'https://db.netkeiba.com/race/list/'
  base_race_url = 'https://db.netkeiba.com'
  cols = ["url"]
  df = pd.DataFrame(columns=cols)
  
  def __init__(self, race_date, date_dir, data_grades_dir, *args, **kwargs):
    super(CollUrlSpider, self).__init__(*args, **kwargs)
    self.start_urls = [self.base_list_url + race_date + '01']
    self.race_date = race_date
    self.date_dir = date_dir
    self.data_grades_dir = data_grades_dir

  def parse(self, response):
    sel = Selector(response)
    calendar_url = sel.css("div[class='race_calendar'] table[summary='レーススケジュールカレンダー'] a::attr(href)").getall()

    for url in calendar_url:
      print("============================")
      print("■デバッグ")
      print("============================")
      url = 'https://db.netkeiba.com' + url
      print(url)
      yield scrapy.Request(url, self.coll_url)
  
  def coll_url(self, response):
    sel = Selector(response)
    race_url = sel.css("div[id='contents'] div[class='race_list fc'] dl[class='race_top_data_info fc'] dd>a::attr(href)").getall()
    for url in race_url:
      url = [self.base_race_url + url]
      df_append = pd.DataFrame(data=url, columns=self.cols)
      self.df = pd.concat([self.df, df_append], ignore_index=True, axis=0)
    self.df.to_csv(os.path.join(self.date_dir,self.race_date) + '.csv', index = False)
    print("============================")
    print("■デバッグ")
    print("============================")
    print(self.df)
