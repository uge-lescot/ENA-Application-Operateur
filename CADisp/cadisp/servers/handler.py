from http.server import BaseHTTPRequestHandler
import logging as log
import json
import cgi


class DashboardServerHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for dashboard.

    Only POST JSON is handled. Expected entry are:

     - action: manual/auto_available/autonomous/end_zone/critical/safety_stop
       => Display the corresponding picto and play the corresponding sound
     - action: shutdown
       => Shutdown the server
    """

    # noinspection PyPep8Naming
    def do_POST(self):
        """
        Read the action and send appropriate signal to the dashboard
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype == 'application/json':
            length = int(self.headers.get('content-length'))
            data = json.loads(self.rfile.read(length).decode('utf-8'))
            log.info("Received %s" % str(data))
            try:
                self.server.process_message(data)
            except Exception as e:
                log.error(e)
