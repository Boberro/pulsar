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

    if file_enabled.lower() == 'true':
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
    if console_enabled.lower() == 'true':
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(stream_handler)
    # endregion

    # region Output Logger
    logger_output.setLevel(logging.INFO)

    if output_file_enabled.lower() == 'true':
        output_file_handler = logging.FileHandler(output_path)
        output_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger_output.addHandler(output_file_handler)
    if output_console_enabled.lower() == 'true':
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
        output_to_file = config_parser.get('output logger', 'log_to_file')
        output_to_console = config_parser.get('output logger', 'log_to_console')
        output_file_path = config_parser.get('output logger', 'path')
        log_to_file = config_parser.get('status logger', 'log_to_file')
        log_to_console = config_parser.get('status logger', 'log_to_console')
        logger_file_path = config_parser.get('status logger', 'path')
        log_level = config_parser.get('status logger', 'level')
    except ConfigParser.NoOptionError as e:
        print 'Error: Config file error: {}'.format(e)
    except ConfigParser.NoSectionError as e:
        print 'Error: Config file error: {}. Is {} correct path?'.format(e, config_path)
    else:
        setup_loggers(
            log_to_file, log_to_console, logger_file_path, log_level,
            output_to_file, output_to_console, output_file_path
        )

        try:
            refresh_time = float(refresh_time)
        except ValueError as e:
            logger.error('Incorrect refresh time value in configuration file. Defaulting to 5')
            refresh_time = 5

        try:
            with open(url_list_path, 'rb') as url_list_file:
                url_list_reader = csv.reader(url_list_file, delimiter=';', quotechar="\"")
                url_list = [row for row in url_list_reader]
        except IOError as e:
            logger.error('Could not find url definition file {}'.format(url_list_path))
        else:
            pulsar = Pulsar(refresh_time, url_list)
            pulsar.start()

            try:
                while True:
                    sleep(1)

            except (KeyboardInterrupt, SystemExit):
                pulsar.stop()
