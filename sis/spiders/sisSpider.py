# -*- coding: utf-8 -*-
import scrapy
from sis.items import SisItem
import re
from scrapy.crawler import CrawlerProcess

WEBSITE = 'http://68.168.16.149'
SEARCH = r''
PAGES = '100'

class sisSpider(scrapy.Spider):
    name = 'sis'
    allowed_domains = []

    def __init__(self, search=SEARCH, pages=PAGES, website=WEBSITE, start=None):
        self.search = search
        self.pages = int(pages)
        self.website = website

        if start:
            self.start_urls = [self.website + start]
        else:
            self.start_urls = [self.website + '/forum/forum-426-1.html',
                               self.website + '/forum/forum-143-1.html',
                               self.website + '/forum/forum-230-1.html',
                               self.website + '/forum/forum-25-1.html',
                               self.website + '/forum/forum-58-1.html']

        print("---------------------------------------------------------------------")
        print("Search:{} Pages:{} Website:{} Start:{}".format(search, pages, website, start))
        print("---------------------------------------------------------------------")


    def parse(self, response):

        titles = response.xpath('//table/tbody/tr/th[@class]/span[@id]/a')
        group = response.xpath('//div[@id="nav"]/p[1]/text()').extract_first()
        page = response.xpath('//div[@class="pages"]/strong//text()').extract_first()
        page = int(page) if page else 0
        print("[page-{}] {}".format(page, group))

        for title in titles:
            text = title.xpath("text()").extract_first()
            match = re.search(self.search, text, re.I)
            if match:
                print("√ {}".format(text))
                href = title.xpath("@href").extract_first()
                yield scrapy.Request(self.website + "/forum/" + href, callback=self.parse_album)

        if page < self.pages:
            new_url= response.xpath('//div[@class="pages"]/a[@class="next"]//@href').extract_first()
            if new_url:
                yield scrapy.Request(self.website + "/forum/" + new_url, callback=self.parse)


    def parse_album(self, response):
        group = response.xpath('//div[@id="nav"]/a[2]/text()').extract_first()
        title = response.xpath('//div[@class="postmessage defaultpost"]/h2/text()').extract_first()

        if group and title:
            try:
                attach = response.xpath('//dl[@class="t_attachlist"]/dt/a[2]')
                torrent_url = self.website + '/forum/' + attach.xpath('@href').extract_first()
                torrent_name = attach.xpath('text()').extract_first()
            except Exception as e:
                print("Exception: No torrent ({})".format(title))
                torrent_url = ''
                torrent_name = ''

            images = response.xpath('//div[@class="t_msgfont"]//img/@src').extract()
            image = []
            for i in images:
                if not re.search(r'\.gif$', i) and re.search(r'^http', i):
                    image.append(i)

            item = SisItem()
            item['album'] = dict(group=group, title=title, torrent_url=torrent_url, torrent_name=torrent_name, image=image)
            yield item
