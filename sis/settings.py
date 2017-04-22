# -*- coding: utf-8 -*-
 
# Scrapy settings for sis project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sis'

SPIDER_MODULES = ['sis.spiders']
NEWSPIDER_MODULE = 'sis.spiders'

ITEM_PIPELINES = {
   'sis.pipelines.SisPipeline': 1,
}

