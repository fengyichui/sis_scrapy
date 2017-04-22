# -*- coding: utf-8 -*-
import scrapy
from sis.items import SisItem
import re
 
from scrapy.crawler import CrawlerProcess

WEBSITE = 'http://68.168.16.149/'
SEARCH = r'parm'
PAGES = 2

class sisSpider(scrapy.Spider):
    name = 'sis'
    allowed_domains = []
    start_urls = [WEBSITE + "forum/forum-58-1.html"]
    ipage = 0

    def parse(self, response):
        titles = response.xpath('//table/tbody/tr/th[@class="new" or @class="common"]/span[@id]/a')
        for title in titles:
            text = title.xpath("text()").extract()[0]
#            print(text)
            match = re.search(SEARCH, text, re.I)
            if match:
                href = title.xpath("@href").extract()[0]
#                print(text)
                yield scrapy.Request(WEBSITE + "forum/" + href, callback=self.parse_album)
        self.ipage += 1
        if self.ipage < PAGES:
            # Next page
            new_url= response.xpath('//a[@class="next"]//@href').extract()[0]
            if new_url:
                yield scrapy.Request(WEBSITE + "forum/" + new_url, callback=self.parse)

    def parse_album(self, response):
        item = SisItem()
        attach = response.xpath('//dl[@class="t_attachlist"]/dt/a[2]')
        title = response.xpath('//div[@class="postmessage defaultpost"]/h2/text()').extract()[0]
        image = response.xpath('//div[@class="t_msgfont"]//img/@src').extract()
        torrent_url = WEBSITE + 'forum/' + attach.xpath('@href').extract()[0]
        torrent_name = attach.xpath('text()').extract()[0]
        album = dict(title=title, torrent_url=torrent_url, torrent_name=torrent_name, image=image)
        item['album'] = album
#        print(album)
        yield item
