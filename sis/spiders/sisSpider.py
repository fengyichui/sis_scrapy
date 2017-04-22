# -*- coding: utf-8 -*-
import scrapy
from sis.items import SisItem
import re
 
from scrapy.crawler import CrawlerProcess

WEBSITE = 'http://68.168.16.149/'
SEARCH = r'合集'
PAGES = 10

class sisSpider(scrapy.Spider):
    name = 'sis'
    allowed_domains = []
    start_urls = [WEBSITE + 'forum/forum-426-1.html',
                  WEBSITE + 'forum/forum-143-1.html',
                  WEBSITE + 'forum/forum-230-1.html',
                  WEBSITE + 'forum/forum-25-1.html',
                  WEBSITE + 'forum/forum-58-1.html']


    def parse(self, response):
        titles = response.xpath('//table/tbody/tr/th[@class="new" or @class="common"]/span[@id]/a')
        page = response.xpath('//div[@class="pages"]/strong//text()').extract()
        page = int(page[0]) if page else 0

        for title in titles:
            text = title.xpath("text()").extract()[0]
            match = re.search(SEARCH, text, re.I)
            if match:
                print("√ [page-{}] {}".format(page, text))
                href = title.xpath("@href").extract()[0]
                yield scrapy.Request(WEBSITE + "forum/" + href, callback=self.parse_album)

        if page < PAGES:
            new_url= response.xpath('//div[@class="pages"]/a[@class="next"]//@href').extract()[0]
            if new_url:
                yield scrapy.Request(WEBSITE + "forum/" + new_url, callback=self.parse)


    def parse_album(self, response):
        group = response.xpath('//div[@id="nav"]/a[2]/text()').extract()[0]
        title = response.xpath('//div[@class="postmessage defaultpost"]/h2/text()').extract()[0]
        images = response.xpath('//div[@class="t_msgfont"]//img/@src').extract()
        attach = response.xpath('//dl[@class="t_attachlist"]/dt/a[2]')
        torrent_url = WEBSITE + 'forum/' + attach.xpath('@href').extract()[0]
        torrent_name = attach.xpath('text()').extract()[0]

        image = []
        for i in images:
            if not re.search(r'\.gif$', i) and re.search(r'^http', i):
                image.append(i)

        item = SisItem()
        item['album'] = dict(group=group, title=title, torrent_url=torrent_url, torrent_name=torrent_name, image=image)
        yield item
