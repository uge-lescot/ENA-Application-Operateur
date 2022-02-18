import json
import zmq
import logging as log

from .server import CadispServer


class ThreadedZMQServer(CadispServer):
    """
    Implements a ZMQ Pull server
    """

    # noinspection PyUnresolvedReferences
    def __init__(self, ip='127.0.0.1', port=9308, parent=None):
        CadispServer.__init__(self, parent)
        url = "tcp://" + ip + ":" + str(port)

        self.context = zmq.Context()

        #  Socket to talk to server
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind(url)

    def run(self):
        while True:
            #  Wait for next request from client
            data_json = self.socket.recv_string()
            log.info("Received %s" % data_json)
            data = json.loads(data_json)
            self.process_message(data)
