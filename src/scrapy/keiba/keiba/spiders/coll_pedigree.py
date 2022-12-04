import scrapy
from scrapy.selector import Selector
import pandas as pd
import os
import re

class CollPedigreeSpider(scrapy.Spider):
  name = 'coll_pedigree'
  allowed_domains = ['db.netkeiba.com']
  start_urls = ['https://db.netkeiba.com/horse/ped/2018105074/']
  
  def parse(self, response):
    sel = Selector(response)
    ped_info = sel.css("table[class='blood_table detail'] tr td")
    for ped in ped_info:
      ped1 = ped.css("::text").getall()
      ped_list = [re.sub(r'\n','',i) for i in ped1]
      print(''.join(ped_list))
      #print(ped.css("::text").getall())
