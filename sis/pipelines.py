# -*- coding: utf-8 -*-
 
import os
import urllib
 
from sis import settings
 
DIR = './save/'

class SisPipeline(object):
 
    def process_item(self, item, spider):
        if not os.path.exists(DIR):
            os.makedirs(DIR)
        dir = DIR + item['album']['title']
        if not os.path.exists(dir):
            os.makedirs(dir)
        urllib.request.urlretrieve(item['album']['torrent_url'],
                "{}/{}".format(dir,item['album']['torrent_name']))
        for image_url in item['album']['image']:
            list_name = image_url.split('/')
            file_name = list_name[len(list_name)-1]
            urllib.request.urlretrieve(image_url, '{}/{}'.format(dir,file_name))
        return item
