from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import pandas as pd

process = CrawlerProcess(get_project_settings())
process.crawl('grades', domain='www.jra.go.jp')
process.start()
