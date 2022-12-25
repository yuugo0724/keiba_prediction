import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

args = sys.argv

url = args[1]
pred_dir = args[2]

process = CrawlerProcess(get_project_settings())
process.crawl('coll_pred_grades', domain='https://db.netkeiba.com/', url=url, pred_dir=pred_dir)
process.start()

