from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from jinja2 import Template
import logging
import sys

logger = logging.getLogger('pulsar')


class PulsarWebInterfaceServer(HTTPServer):
    def __init__(self, address, port, parent):
        self.parent = parent

        try:
            with open('templates/index.jinja2', 'rb') as f:
                self.template = Template(f.read())
        except IOError as e:
            logger.error('Web interface template file not found. Web interface not staring.')
            self.template = None

        HTTPServer.__init__(self, (address, port), PulsarWebInterfaceHandler)


class PulsarWebInterfaceHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            self.server.template.render(
                refresh_time=self.server.parent.refresh_time,
                stats=self.server.parent.latest_stats)
        )
