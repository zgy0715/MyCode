import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from douban_crawler.spiders.douban_top250 import DoubanTop250Spider

print("爬虫启动中 ...")
process = CrawlerProcess(get_project_settings())
process.crawl(DoubanTop250Spider)
process.start()
