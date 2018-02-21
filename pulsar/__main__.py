# -*- coding: utf-8 -*-
import sys
import requests
import time
import ConfigParser
import csv
from pulsar import run_pulsar


def _requests(url):
    t1 = time.time()
    r = requests.get(url)
    t2 = time.time()
    return t2 - t1, r.elapsed


if __name__ == '__main__':
    try:
        config_path = sys.argv[1]
    except IndexError:
        print 'Warning: No configuration file path given. Trying "config.ini"'
        config_path = 'config.ini'

    config_parser = ConfigParser.ConfigParser()
    config_parser.read(config_path)

    try:
        refresh_time = config_parser.get('main', 'refresh_time')
        url_list_path = config_parser.get('main', 'url_list_path')
    except ConfigParser.NoOptionError as e:
        print 'Error: Config file error: {}'.format(e)
    except ConfigParser.NoSectionError as e:
        print 'Error: Config file error: {}. Is {} correct path?'.format(e, config_path)
    else:
        try:
            with open(url_list_path, 'rb') as url_list_file:
                url_list_reader = csv.reader(url_list_file, delimiter=';', quotechar="\"")
                url_list = [row for row in url_list_reader]
        except IOError as e:
            print 'Error: Could not find url definition file {}'.format(url_list_path)
        else:
            run_pulsar(refresh_time, url_list)

    print "Pulsar closed."

    # print _requests('http://www.rarlab.com/rar/winrar-x64-420.exe')
