# -*- coding: utf-8 -*-
# just for ip address testing purposes

import scrapy
import logging
from bs4 import BeautifulSoup

class IPTesterSpider(scrapy.Spider):
    name = 'IPtester'
    allowed_domains = ['whatismyipaddress.com']
    start_urls = (
        'http://whatismyipaddress.com/',
    )

    def parse(self, response):
    	soup = BeautifulSoup(response.body, 'html.parser')

        ip_container = soup.select('#section_left > div:nth-of-type(2) > a:nth-of-type(1)')
        if len(ip_container) > 0:
            try:
                ip_container = ip_container[0].encode('UTF-8')
                ip = BeautifulSoup(ip_container, 'html.parser').get_text()
                logging.info('IP ADDRESS = %s' % ip)
            except (RuntimeError, IndexError):
                logging.info('IP ADDRESS NOT FOUND')
        pass
