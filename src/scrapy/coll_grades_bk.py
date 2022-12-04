import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

args = sys.argv

base_dir = args[1]
grades_dir = args[2]

os.chdir(grades_dir)

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl('race_result')
process.start()

# main.ipynbのパスに戻る
os.chdir(base_dir)
