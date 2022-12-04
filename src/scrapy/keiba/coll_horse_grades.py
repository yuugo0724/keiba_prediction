import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

args = sys.argv

horse_id = args[1]
data_master_horse_grades = args[2]

process = CrawlerProcess(get_project_settings())
process.crawl('coll_horse_grades', domain='https://db.netkeiba.com/', horse_id=horse_id, data_master_horse_grades=data_master_horse_grades)
process.start()

