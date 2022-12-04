import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

args = sys.argv

race_date = args[1]
date_dir = args[2]
data_grades_dir = args[3]

process = CrawlerProcess(get_project_settings())
process.crawl('coll_url', domain='https://db.netkeiba.com/', race_date=race_date, date_dir=date_dir, data_grades_dir=data_grades_dir)
process.start()

