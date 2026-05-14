import scrapy
import re
from datetime import datetime
from douban_crawler.items import DoubanMovieItem


class DoubanTop250Spider(scrapy.Spider):
    name = "douban_top250"
    allowed_domains = ["movie.douban.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_url = "https://movie.douban.com/top250?start={}&filter="
        self.start_urls = [base_url.format(i * 25) for i in range(10)]

    def parse(self, response):
        for item in response.css(".item"):
            movie = DoubanMovieItem()
            movie["title"] = item.css(".title::text").get("").strip()
            movie["score"] = item.css(".rating_num::text").get("").strip()

            # 评分人数（跟在 rating_num 后的 span 文本取数字）
            rating_span = item.xpath(".//span[@class='rating_num']/following-sibling::span/text()").get("")
            m = re.search(r"(\d+)", rating_span)
            movie["rating_num"] = m.group(1) if m else "0"

            movie["quote"] = item.css(".quote span::text").get("") or "无评语"
            movie["poster_url"] = item.css(".pic img::attr(src)").get("")
            movie["page_url"] = item.css(".hd a::attr(href)").get("")
            movie["crawl_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self._parse_bd(item, movie)
            yield movie

    def _parse_bd(self, item, movie):
        """从 .bd p HTML 中解析导演、主演、年份、地区、类型、片长"""
        html = item.css(".bd p").get()
        if not html:
            return

        # 按 <br> 拆分行
        lines = re.split(r"<br\s*/?>", html, flags=re.IGNORECASE)
        lines = [re.sub(r"<[^>]+>", "", l).strip() for l in lines if l.strip()]

        # 第一行：导演 / 主演
        if lines:
            line1 = lines[0]
            # 用 `主演:` 分割来分离导演和主演
            if "导演:" in line1:
                movie["directors"] = line1.split("导演:")[1].split("主演:")[0].strip().rstrip("\xa0").strip()
            if "主演:" in line1:
                movie["actors"] = line1.split("主演:")[1].strip()

        # 第二行：年份 / 地区 / 类型 / 片长
        if len(lines) > 1:
            parts = [p.strip() for p in re.split(r"\s*/\s*", lines[1]) if p.strip()]
            for p in parts:
                if re.match(r"^\d{4}", p):
                    movie["year"] = re.search(r"(\d{4})", p).group(1)
                elif re.search(r"\d+分钟", p):
                    movie["duration"] = re.search(r"(\d+分钟)", p).group(1)
                elif re.search(r"[一-鿿]", p) and not re.search(r"分钟", p):
                    if not movie.get("region"):
                        movie["region"] = p
                    elif not movie.get("genres"):
                        movie["genres"] = p
