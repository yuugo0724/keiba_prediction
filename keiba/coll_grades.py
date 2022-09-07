from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import pandas as pd

if os.path.isfile("grades_urls.txt"):
  os.system("rm -rf grades_urls.txt")
os.system("touch grades_urls.txt")
process = CrawlerProcess(get_project_settings())
process.crawl('grades_url', domain='www.jra.go.jp')
process.start()
with open('grades_urls.txt', 'r') as f:
  csv_list = f.read().splitlines()
df = pd.DataFrame(csv_list, columns = ['url'])
df_del = df.drop_duplicates()
df_s = df_del.sort_values('url')
df_s.to_csv('grades_urls.csv', header=False, index=False)
