# -*- coding: utf-8 -*-
import requests
from requests.exceptions import ConnectionError
import time
import logging


logger = logging.getLogger('pulsar')
logger_output = logging.getLogger('pulsar_output')

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
            logger_output.warning('{} connection error'.format(url))
        else:
            total_time = t2 - t1
            logger_output.info('{} total time: {}s'.format(url, total_time))

    def start(self):
        logger.info('Starting pulsar')
        for url, text_to_find in self.url_list:
            self.check_url(url, text_to_find)
