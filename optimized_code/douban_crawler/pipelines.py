import csv
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class CsvPipeline:
    """数据存储为 CSV"""

    def open_spider(self, spider):
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filepath = f"output/douban_top250_{timestamp}.csv"
        self.file = open(self.filepath, "w", newline="", encoding="utf-8-sig")
        self.writer = csv.DictWriter(self.file, fieldnames=[
            "title", "score", "rating_num", "genres", "year",
            "region", "directors", "actors", "duration", "quote",
            "summary", "poster_url", "page_url", "crawl_time",
        ])
        self.writer.writeheader()
        logger.info(f"CSV 输出: {self.filepath}")

    def close_spider(self, spider):
        self.file.close()
        logger.info(f"数据已保存: {self.filepath}")

    def process_item(self, item, spider):
        self.writer.writerow(dict(item))
        return item
