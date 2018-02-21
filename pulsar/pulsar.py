# -*- coding: utf-8 -*-
class Pulsar(object):
    def __init__(self, refresh_time, url_list):
        self.refresh_time = refresh_time
        self.url_list = url_list

    def start(self):
        print "start", self.refresh_time, self.url_list
