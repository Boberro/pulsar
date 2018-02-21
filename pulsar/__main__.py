# -*- coding: utf-8 -*-
import sys
import ConfigParser
import csv
import logging
from pulsar import Pulsar


def setup_logger(path, level):
    if level.lower() == 'debug':
        level = logging.DEBUG
    elif level.lower() == 'info':
        level = logging.INFO
    elif level.lower() == 'warn':
        level = logging.WARN
    else:
        print 'Warning: Incorrect log level set in configuration file. Using WARN level instead.'
        level = logging.WARN

    logger = logging.getLogger('pulsar')
    logger.setLevel(level)
    logging.basicConfig(filename=path, level=level)


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
        log_path = config_parser.get('logging', 'log_path')
        log_level = config_parser.get('logging', 'log_level')
    except ConfigParser.NoOptionError as e:
        print 'Error: Config file error: {}'.format(e)
    except ConfigParser.NoSectionError as e:
        print 'Error: Config file error: {}. Is {} correct path?'.format(e, config_path)
    else:
        setup_logger(log_path, log_level)

        try:
            with open(url_list_path, 'rb') as url_list_file:
                url_list_reader = csv.reader(url_list_file, delimiter=';', quotechar="\"")
                url_list = [row for row in url_list_reader]
        except IOError as e:
            logging.warning('Error: Could not find url definition file {}'.format(url_list_path))
        else:
            pulsar = Pulsar(refresh_time, url_list)
            pulsar.start()

    print "Pulsar closed."

    # print _requests('http://www.rarlab.com/rar/winrar-x64-420.exe')
