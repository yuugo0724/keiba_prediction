from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import pandas as pd

if os.path.isfile("grades_urls.txt"):
  os.system("rm -rf grades_urls.txt")

if os.path.isfile("grades_urls.csv"):
  os.system("rm -rf grades_urls.csv")

process = CrawlerProcess(get_project_settings())
process.crawl('grades_url', domain='www.jra.go.jp')
process.start()

with open('grades_urls.txt', 'r') as f:
  csv_list = f.read().splitlines()

df = pd.DataFrame(csv_list, columns = ['URL'])
df_del = df.drop_duplicates()
df_s = df_del.sort_values('URL')
df_s.to_csv('grades_urls.csv', header="URL", index=False)
