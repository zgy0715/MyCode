import scrapy


class DoubanMovieItem(scrapy.Item):
    title = scrapy.Field()
    score = scrapy.Field()
    rating_num = scrapy.Field()
    genres = scrapy.Field()
    year = scrapy.Field()
    region = scrapy.Field()
    directors = scrapy.Field()
    actors = scrapy.Field()
    duration = scrapy.Field()
    quote = scrapy.Field()
    summary = scrapy.Field()
    poster_url = scrapy.Field()
    page_url = scrapy.Field()
    crawl_time = scrapy.Field()
