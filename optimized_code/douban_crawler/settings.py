BOT_NAME = "douban_crawler"

SPIDER_MODULES = ["douban_crawler.spiders"]
NEWSPIDER_MODULE = "douban_crawler.spiders"

# 异步并发（原始方案为单线程串行）
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# 请求间隔 + 随机化，降低被封风险
DOWNLOAD_DELAY = 2.5
RANDOMIZE_DOWNLOAD_DELAY = True

# 自动重试（原始方案仅 try-except，失败即跳过）
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429, 403]

# URL 去重
DUPEFILTER_CLASS = "scrapy.dupefilters.RFPDupeFilter"

# 中间件
DOWNLOADER_MIDDLEWARES = {
    "douban_crawler.middlewares.RandomUserAgentMiddleware": 100,
    "douban_crawler.middlewares.ProxyMiddleware": 200,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 500,
}

# 管道
ITEM_PIPELINES = {
    "douban_crawler.pipelines.CsvPipeline": 200,
}

# 日志
LOG_ENABLED = True
LOG_LEVEL = "INFO"
LOG_FILE = "logs/crawler.log"

# 请求头
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}

# 不遵守 robots.txt（分析需求下）
ROBOTSTXT_OBEY = False

DOWNLOAD_TIMEOUT = 15
COOKIES_ENABLED = True
CLOSESPIDER_ITEMCOUNT = 250
