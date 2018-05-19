# -*- coding: utf-8 -*-
 
import os
import urllib
import socket
import re
import time
from sis import settings

DIR = './save/' + time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time())) + '/'

socket.setdefaulttimeout(30)

class SisPipeline(object):

    def trim_filename(self, filename):
        return re.sub(r'[\/\\\:\*\?\"\<\>\|]', '-', filename)

    def process_item(self, item, spider):
        if not os.path.exists(DIR):
            os.makedirs(DIR)

        dir = DIR + self.trim_filename(item['album']['group']) + '/' + self.trim_filename(item['album']['title'])
        if not os.path.exists(dir):
            os.makedirs(dir)

        if item['album']['torrent_name']:
            try:
                urllib.request.urlretrieve(item['album']['torrent_url'], "{}/{}".format(dir,item['album']['torrent_name']))
            except Exception as e:
                print("Exception: {} ({})".format(str(e), item['album']['torrent_url']))

        for image_url in item['album']['image']:
            list_name = image_url.split('/')
            file_name = list_name[len(list_name)-1]
            try:
                urllib.request.urlretrieve(image_url, '{}/{}'.format(dir,file_name))
            except Exception as e:
                print("Exception: {} ({})".format(str(e), image_url))

        return item
