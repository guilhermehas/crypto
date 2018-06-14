import sys
sys.path.append('./src')

import flask

from threading import Thread
import wsgiref
import socket

from main import get_server

def get_application(args):
    port = args.port
    class Configuration(object):
        TEST_SERVER_PORT = port

    application = get_server(args)
    application.config.from_object(Configuration)

    return application

def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port

class ServerThread(Thread):
    def setup(self, args):
        self.port = get_free_port()
        args.port = self.port
        self.application = get_application(args)
        self.application.config['TESTING'] = True
        self.port = self.application.config['TEST_SERVER_PORT']

    def run(self):
        self.httpd = wsgiref.simple_server.make_server('localhost', self.port, self.application)
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()

    def make_url(self, endpoint, **kwargs):
        with self.application.app_context():
            return flask.url_for(endpoint, **kwargs)

