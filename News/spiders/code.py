#coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from News.items import NewsItem
import logging
import re
import urllib
import time
import datetime
from scrapy.utils.project import get_project_settings

class NewsSpider(CrawlSpider):

    name = 'news'
    allowed_domains = ['chinanews.com']

    rules = (
            Rule(LinkExtractor(allow = ('chinanews.com\/\w+\/\d{4}\/\d{2}-\d{2}\/\d+.shtml',), deny = ('chinanews.com\/tp\/\d{4}\/\d{2}-\d{2}\/\d+.shtml',)), callback = 'parse_info', follow = False),
            )

    def __init__(self, *a, **kw):
        super(CrawlSpider, self).__init__(*a, **kw)
        self.settings = get_project_settings()
        self.begin_date      = self.settings['BEGIN_DATE']
        self.end_date        = self.settings['END_DATE']
        self.type_list       = self.settings['TYPE_LIST']
        self._compile_rules()
        self.start_urls      = self.Start_urls()

    def start_requests(self):
        url_list = self.Start_urls()
        for url in url_list:
            yield self.make_requests_from_url(url)

    def Start_urls(self):

        url_list = []
        date_list = self.GetBetweenDay()
        #url = "http://www.chinanews.com/scroll-news/"+ "it" + "/2012/0602" + "/news.shtml"
        for news_type in self.type_list:
            url = "http://www.chinanews.com/scroll-news/" + news_type
            for news_date in date_list:
                URL = url + news_date + "/news.shtml"
                url_list.append(URL)

        return url_list

    def GetBetweenDay(self):

        date_list = []
        begin_date = datetime.datetime.strptime(self.begin_date, "%Y%m%d")
        end_date = datetime.datetime.strptime(self.end_date, "%Y%m%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("/%Y/%m%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)

        return date_list

    def parse_info(self, response):

        item = NewsItem()
        sel = Selector(response)

        url = response.url
        regex1 = '\d{4}\/\d{2}-\d{2}'
        regex2 = '\d+(?=\.)'
        regex3 = '(?<=\/)\w+(?=\/)'
        regex4 = '(\\n)+'
        match1 = re.search(regex1, url)
        match2 = re.search(regex2, url)
        match3 = re.search(regex3, url)
        item['news_date'] = match1.group().replace('-','').replace('/','')
        item['news_id'] = match2.group()
        item['news_type'] = match3.group()

        str1 = sel.xpath('//*[@id="cont_1_1_2"]/h1/text()').extract_first().replace('\r\n', '').replace('\n','')
        item['news_title'] = str1.encode('utf-8')

        data2 = sel.xpath('//*[@id="cont_1_1_2"]/div[@class="left_zw"]')
        jsstr = '_acM({aid:"mm_122588615_24060014_79798355",format:1,mode:1,gid:1,serverbaseurl:"afpeng.alimama.com/"});'
        str2 = data2[0].xpath('string(.)').extract()[0].replace('\r\n','\n').replace(jsstr,'')
        str2 = re.sub(regex4, '\n', str2)
        item['news_text'] = str2.encode('utf-8')

        yield item
