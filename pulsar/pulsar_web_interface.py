from BaseHTTPServer import BaseHTTPRequestHandler
import threading
import time

HOST_NAME = ''
PORT_NUMBER = 8080


class PulsarWebInterfaceHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>It works!</title></head>")
        s.wfile.write("<body><h1>It works!</h1></body></html>")
