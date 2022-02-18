from http.server import HTTPServer

from .server import CadispServer
from .handler import DashboardServerHandler


class ThreadedHTTPServer(HTTPServer, CadispServer):

    def __init__(self, port=26686, parent=None):
        CadispServer.__init__(self, parent)
        HTTPServer.__init__(self, ("", port), DashboardServerHandler)

    def run(self):
        self.serve_forever()
