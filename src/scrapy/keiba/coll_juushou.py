import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

args = sys.argv

juushou_year = args[1]
data_juushou_list = args[2]

process = CrawlerProcess(get_project_settings())
process.crawl('coll_juushou', domain='https://db.netkeiba.com/', juushou_year=juushou_year, data_juushou_list=data_juushou_list)
process.start()

