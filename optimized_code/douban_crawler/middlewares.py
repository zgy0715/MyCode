import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 "
    "Firefox/133.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/18.0 Safari/605.1.15",
]

PROXY_POOL = []


class RandomUserAgentMiddleware:
    """随机 User-Agent 和请求头，模拟真实浏览器"""

    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(USER_AGENTS)
        request.headers["Accept"] = (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/webp,*/*;q=0.8"
        )
        request.headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8"
        request.headers["Cache-Control"] = "no-cache"
        request.headers["Referer"] = "https://movie.douban.com/"


class ProxyMiddleware:
    """代理 IP 轮换"""
    # 如需使用代理，往 PROXY_POOL 里添加 "http://ip:port"
    # 示例: PROXY_POOL = ["http://127.0.0.1:7890"]

    def process_request(self, request, spider):
        if PROXY_POOL:
            request.meta["proxy"] = random.choice(PROXY_POOL)
