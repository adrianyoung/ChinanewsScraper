# -*- coding: utf-8 -*-

# Scrapy settings for News project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'News'
SPIDER_MODULES = ['News.spiders']
NEWSPIDER_MODULE = 'News.spiders'

# NEWS TYPE SETTINGS
TYPE_LIST         =  # ['wh','mil','gj','yl','ty','jk','sh','hr','fortune','cj','it','ny','ga','estate','auto','tw']

# SPIDERS DATE SETTINGS
BEGIN_DATE        =  # '20120601'
END_DATE          =  # '20170728'

# MYSQL SETTINGS
MYSQL_HOST        =  #'localhost'
MYSQL_USER        =  #'username'
MYSQL_PASSWORD    =  #'password'
MYSQL_DATABASE    =  #'databasename'
# REDIS SETTINGS
REDIS_HOST        =  #'127.0.0.1'
REDIS_PORT        =  #'6379'
REDIS_PASSWORD    =  #'password'
REDIS_DB1         =  #1                  #DUPLICATE URLS
REDIS_DB2         =  #2                  #DUPLICATE ITEMS
# MONGODB SETTINGS
MONGO_URI         =  #'mongodb://usrname:password@127.0.0.1:27017'
MONGO_DATABASE    =  #'databasename'

# TOR SETTINGS
HTTP_PROXY        =  #'http://127.0.0.1:8123'
AUTH_PASSWORD     =  #'secretPassword'
CONTROL_PORT      =  #9051
#number of HTTP request before the IP change
MAX_REQ_PER_IP    =  #80

# DUPLICATE SAVE SETTINGS
#SPECIAL_URLS = ['http://music.163.com/weapi/v1/resource/comments/R_SO_4_185807/?csrf_token=']
#SPECIAL_URLS_RES = [ur'http:\/\/music\.163\.com\/weapi\/v1\/resource\/comments\/R_SO_4_\d+\/\?csrf_token=']

# DUPLICATE FILTER SETTINGS
DUPLICATE_REQUEST_ENABLED = True
DUPLICATE_REQUEST_RESET   = True
DUPLICATE_ITEM_RESET      = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'News (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.15

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

RETRY_TIMES = 2
RETRY_HTTP_CODES = [500, 502, 503, 504]

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'News.middlewares.NewsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'News.middlewares.IngoreRequestMiddleware':310,
    'News.middlewares.RandomUserAgentMiddleware':400,
#    'News.middlewares.TorProxyMiddleware': 410,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    'News.pipelines.RedisDuplicatePipeline': 100,
    'News.pipelines.MongodbPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
