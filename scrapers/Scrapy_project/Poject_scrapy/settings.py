# Scrapy settings for Poject_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "Poject_scrapy"

SPIDER_MODULES = ["Poject_scrapy.spiders"]
NEWSPIDER_MODULE = "Poject_scrapy.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "Poject_scrapy (+http://www.yourdomain.com)"
USER_AGENTS_LIST = [
    {"user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.32","referer": "https://www.google.com"},
    {"user_agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.03","referer": "https://www.google.com"},
    {"user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.13 Safari/603.2.4","referer": "https://www.google.com"},
    {"user_agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.30 Edge/14.14393',"referer": "https://www.google.com"},
    {"user_agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.3',"referer": "https://www.google.co.uk/"},
    {"user_agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.2',"referer": "https://www.google.com.ar/"},
    {"user_agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.3',"referer": "https://www.google.com.br/"},
    {"user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.992","referer": "https://yandex.com/"},
    {"user_agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.10","referer": "https://www.google.com"},
    {"user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.22.04","referer": "https://www.google.com"},
    {"user_agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.3 Edge/14.143933',"referer": "https://www.google.com"},
    {"user_agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.31',"referer": "https://www.google.com"},
    {"user_agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.255',"referer": "https://www.google.com"},
    {"user_agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.5',"referer": "https://www.google.com"},
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS = 5 ###

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 300
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 15 #TROVIMAP

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False ###

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "Poject_scrapy.middlewares.PojectScrapySpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "Poject_scrapy.middlewares.PojectScrapyDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "Poject_scrapy.pipelines.PojectScrapyPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 10
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOADER_MIDDLEWARES = {
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 900,#610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 910,#620,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None, # Disable default user-agent middleware
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 600,#400, # Enable user-agent middleware
    # 'scrapy_selenium.SeleniumMiddleware': 800 ###### selenium
    # 'scrapy_selenium.MySeleniumMiddleware': 800 ###### selenium
    # 'scrapy_cloudflare_middleware.middlewares.CloudFlareMiddleware': 560
}


RETRY_TIMES = 3
# RETRY_HTTP_CODES = [500, 503, 504]
RETRY_HTTP_CODES = [500, 503, 504, 403, 408, 429, 451]


# Saving logs in a file
# setting log level and format
LOG_LEVEL = 'INFO' 
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_FILE = 'logs/scrapy.log'


# Proxy list
# ROTATING_PROXY_LIST = [
#     '45.22.209.157:8888',
    # '41.231.37.76:3128',
    # '8.219.97.248:80',
    # '43.133.59.220:3128',
    # "138.197.102.119:80",
    # "203.150.128.245:8080",
    # "185.108.141.74:8080",
    # "13.37.59.99:3128",
    # "178.212.49.96:1080",
    # "34.64.4.104:80",  
# ]


### TEST ###
# USER_AGENTS_LIST = [
#     {
#         "headers": {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "Accept-Language": "en-US,en;q=0.9",
#             "cache-control": "max-age=0",
#             "priority": "u=0, i",
#             "Referer": "https://www.habitaclia.com/",
#             "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
#             "Sec-Ch-Ua-Mobile": "?0",
#             "Sec-Ch-Ua-Platform": "\"Windows\"",
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "none",
#             "Upgrade-Insecure-Requests": "1",
#             "sec-fetch-user": "?1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.361"
#             }
# },
#     {
#         "headers": {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "Accept-Language": "en-US,en;q=0.9",
#             "cache-control": "max-age=0",
#             "priority": "u=0, i",
#             "Referer": "https://www.habitaclia.com/",
#             "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
#             "Sec-Ch-Ua-Mobile": "?0",
#             "Sec-Ch-Ua-Platform": "\"Windows\"",
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "none",
#             "Upgrade-Insecure-Requests": "1",
#             "sec-fetch-user": "?1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#             }
        
#     },
#     {
#         "headers": {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "Accept-Language": "en-US,en;q=0.9",
#             "cache-control": "max-age=0",
#             "priority": "u=0, i",
#             "Referer": "https://www.habitaclia.com/",
#             "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
#             "Sec-Ch-Ua-Mobile": "?0",
#             "Sec-Ch-Ua-Platform": "\"Windows\"",
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "none",
#             "Upgrade-Insecure-Requests": "1",
#             "sec-fetch-user": "?1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#             }
#     },
#     {
#         "headers": {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "Accept-Language": "en-US,en;q=0.9",
#             "cache-control": "max-age=0",
#             "priority": "u=0, i",
#             "Referer": "https://www.habitaclia.com/",
#             "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
#             "Sec-Ch-Ua-Mobile": "?0",
#             "Sec-Ch-Ua-Platform": "\"Windows\"",
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "none",
#             "Upgrade-Insecure-Requests": "1",
#             "sec-fetch-user": "?1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#             }
#     },
#     {
#         "headers": {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "Accept-Language": "en-US,en;q=0.9",
#             "cache-control": "max-age=0",
#             "priority": "u=0, i",
#             "Referer": "https://www.habitaclia.com/",
#             "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
#             "Sec-Ch-Ua-Mobile": "?0",
#             "Sec-Ch-Ua-Platform": "\"Windows\"",
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "none",
#             "Upgrade-Insecure-Requests": "1",
#             "sec-fetch-user": "?1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#             }
#     },
#         ]


RANDOMIZE_USER_AGENT = True
DOWNLOAD_FAIL_ON_DATALOSS = False #####