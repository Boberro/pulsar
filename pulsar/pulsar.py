# -*- coding: utf-8 -*-
import requests
from requests.exceptions import ConnectionError
import time


class Pulsar(object):
    def __init__(self, refresh_time, url_list):
        self.refresh_time = refresh_time
        self.url_list = url_list

    def check_url(self, url, text_to_find):
        try:
            t1 = time.time()
            r = requests.get(url)
            t2 = time.time()
        except ConnectionError as e:
            print 'Connection error: {}'.format(url)
        else:
            total_time = t2 - t1
            print url, total_time

    def start(self):
        for url, text_to_find in self.url_list:
            self.check_url(url, text_to_find)
