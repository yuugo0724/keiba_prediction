import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

args = sys.argv

url = args[1]
race_id = args[2]
date_dir = args[3]
data_grades_dir = args[4]

process = CrawlerProcess(get_project_settings())
process.crawl('coll_grades', domain='https://db.netkeiba.com/', url=url, race_id=race_id, date_dir=date_dir, data_grades_dir=data_grades_dir)
process.start()

