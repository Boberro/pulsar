# -*- coding: utf-8 -*-
import sys
import ConfigParser
import csv
import logging
from pulsar import Pulsar
from time import sleep

logger = logging.getLogger('pulsar')
logger_output = logging.getLogger('pulsar_output')


def setup_loggers(
        file_enabled, console_enabled, file_path, logger_level,
        output_file_enabled, output_console_enabled, output_path):
    def get_level(level):
        if level.lower() == 'debug':
            return logging.DEBUG
        elif level.lower() == 'info':
            return logging.INFO
        elif level.lower() == 'warn':
            return logging.WARN
        elif level.lower() == 'error':
            return logging.ERROR
        else:
            print 'Warning: Incorrect log level set in configuration file. Using ERROR level instead.'
            return logging.ERROR

    # region Status Logger
    logger.setLevel(get_level(logger_level))

    if file_enabled:
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
    if console_enabled:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(stream_handler)
    # endregion

    # region Output Logger
    logger_output.setLevel(logging.INFO)

    if output_file_enabled:
        output_file_handler = logging.FileHandler(output_path)
        output_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger_output.addHandler(output_file_handler)
    if output_console_enabled:
        output_stream_handler = logging.StreamHandler()
        output_stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger_output.addHandler(output_stream_handler)
    # endregion


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
        output_to_file = config_parser.get('output logger', 'log_to_file').lower() == 'true'
        output_to_console = config_parser.get('output logger', 'log_to_console').lower() == 'true'
        output_file_path = config_parser.get('output logger', 'path')
        log_to_file = config_parser.get('status logger', 'log_to_file').lower() == 'true'
        log_to_console = config_parser.get('status logger', 'log_to_console').lower() == 'true'
        logger_file_path = config_parser.get('status logger', 'path')
        log_level = config_parser.get('status logger', 'level')
        web_interface_enabled = config_parser.get('web interface', 'enabled').lower() == 'true'
        web_interface_address = config_parser.get('web interface', 'address')
        web_interface_port = config_parser.get('web interface', 'port')
    except ConfigParser.NoOptionError as e:
        print 'Error: Config file error: {}'.format(e)
        sys.exit()
    except ConfigParser.NoSectionError as e:
        print 'Error: Config file error: {}. Is {} correct path?'.format(e, config_path)
        sys.exit()

    setup_loggers(
        log_to_file, log_to_console, logger_file_path, log_level,
        output_to_file, output_to_console, output_file_path
    )

    try:
        refresh_time = float(refresh_time)
    except ValueError as e:
        logger.error('Incorrect refresh time value in configuration file.')
        sys.exit()

    try:
        with open(url_list_path, 'rb') as url_list_file:
            url_list_reader = csv.reader(url_list_file, delimiter=';', quotechar="\"")
            url_list = [row for row in url_list_reader]
    except IOError as e:
        logger.error('Could not find url definition file {}'.format(url_list_path))
        sys.exit()

    try:
        web_interface_enabled = config_parser.get('web interface', 'enabled').lower() == 'true'
    except ConfigParser.NoOptionError as e:
        web_interface_enabled = False
    except ConfigParser.NoSectionError as e:
        web_interface_enabled = False

    if web_interface_enabled:
        try:
            web_interface_address = config_parser.get('web interface', 'address')
            web_interface_port = config_parser.get('web interface', 'port')
        except ConfigParser.NoOptionError as e:
            print 'Error: Config file error: {}'.format(e)
            sys.exit()
        except ConfigParser.NoSectionError as e:
            print 'Error: Config file error: {}. Is {} correct path?'.format(e, config_path)
            sys.exit()

        try:
            web_interface_port = int(web_interface_port)
        except ValueError as e:
            logger.error('Incorrect web interface value in configuration file.')
            sys.exit()

    pulsar = Pulsar(refresh_time, url_list, web_interface_address, web_interface_port)
    pulsar.start()

    if web_interface_enabled:
        pulsar.start_web_interface()

    try:
        while True:
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pulsar.stop()
        pulsar.stop_web_interface()
