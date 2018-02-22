# -*- coding: utf-8 -*-
import requests
from requests.exceptions import ConnectionError
import time
import logging
import threading
from pulsar_web_interface import PulsarWebInterfaceServer

logger = logging.getLogger('pulsar')
logger_output = logging.getLogger('pulsar_output')


class Pulsar(object):
    def __init__(self, refresh_time, url_list, web_interface_address, web_interface_port):
        self.refresh_time = refresh_time
        self.url_list = url_list

        self.pulsar_thread = None
        self.pulsar_thread_stop_trigger = None

        self.pulsar_web_interface_thread = None
        self.web_interface_server = None
        self.web_interface_address = web_interface_address
        self.web_interface_port = web_interface_port

        self.latest_stats = {k: {'status': '', 'message': ''} for k in [e[0] for e in url_list]}

    def _pulsar_thread_method(self):
        while not self.pulsar_thread_stop_trigger.is_set():
            logger.debug('Checking websites...')
            for url, text_to_find in self.url_list:
                logger.debug('Checking {} and looking for {}...'.format(url, text_to_find))
                try:
                    t1 = time.time()
                    r = requests.get(url)
                    t2 = time.time()
                except ConnectionError as e:
                    logger_output.warning('{}: connection error'.format(url))
                    self.latest_stats[url] = {
                        'status': 'Problem',
                        'message': 'Could not connect',
                    }
                    continue

                total_time = t2 - t1
                text_found = r.text.find(text_to_find) > -1

                if text_found:
                    logger_output.info('{}: {} {}, text found, total time: {}s'.format(
                        url, r.status_code, r.reason, total_time))
                    self.latest_stats[url] = {
                        'status': 'OK',
                        'message': 'total time: {}'.format(total_time),
                    }
                else:
                    logger_output.warning('{}: {} {}, text not found, total time: {}s'.format(
                        url, r.status_code, r.reason, total_time))
                    self.latest_stats[url] = {
                        'status': 'Problem',
                        'message': 'Text not found. Total time: {}'.format(total_time),
                    }

            logger.debug('Sleeping...')
            time.sleep(self.refresh_time)

    def start(self):
        if self.pulsar_thread is None:
            logger.info('Starting pulsar')
            self.pulsar_thread_stop_trigger = threading.Event()
            self.pulsar_thread = threading.Thread(
                target=self._pulsar_thread_method, args=()
            )
            self.pulsar_thread.start()

    def stop(self):
        if self.pulsar_thread is not None:
            logger.info('Pulsar stopping...')
            self.pulsar_thread_stop_trigger.set()

    def start_web_interface(self):
        if self.pulsar_web_interface_thread is None:
            logger.info('Creating web interface')
            self.web_interface_server = PulsarWebInterfaceServer(
                self.web_interface_address, self.web_interface_port, self)
            self.pulsar_web_interface_thread = threading.Thread(target=self.web_interface_server.serve_forever)
            self.pulsar_web_interface_thread.daemon = True
            if self.web_interface_server.template is not None:
                logger.info('Starting web interface')
                self.pulsar_web_interface_thread.start()
