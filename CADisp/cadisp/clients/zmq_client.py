import zmq
from time import sleep
import csv
from PyQt5 import QtCore
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

#on travaille en reseau local (localhost: 127.0.0.1)
IP_ADRESS = '127.0.0.1'
ZMQ_PORT = 9308


class PushClient:
    """
    La classe
    """

    # constructeur
    def __init__(self, ip=IP_ADRESS, port=ZMQ_PORT):
        self.url = "tcp://" + ip + ":" + str(port)
        self.context = zmq.Context()
        # Socket to talk to server
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.setsockopt(zmq.LINGER, 0)  # To avoid hanging infinitely, particularly when closing the socket
        self.socket.connect(self.url)
        self.fileCsvName = 'parDefaut.csv'

    def sendFileCsvName(self, fileCsvName):
        """
        Ajoute le nom du fichier de dashboard comme propriété de cette classe zmq_client
        :param fileCsvName:
        :return:
        """
        self.fileCsvName = fileCsvName



    def send(self, dataDict,name):
        """
        envoi des données vers le csv
        :param data: Python dict
        :return:
        """

        ### traduction des données reçues sous forme de dictionnaires en ligne de csv
        if dict is not None:
            with open(self.fileCsvName, 'a+') as f: #ecriture en mode "a+" pour ajout en mode append
                writer = csv.writer(f)
                v1 = dataDict.get('TC')
                print(v1)
                v2 = dataDict.get('click')
                print(v2)
                v3 = dataDict.get('donnee')
                print(v3)
                v4 = dataDict.get('numNavette')
                print(v1)
                v5 = dataDict.get('nbPassagers')

                writer.writerow([v1, v2, v3, v4,v5])

        sleep(0.1)

    def quit(self):
        """
        tout fermer
        :return:
        """
        self.socket.close()
        self.context.term()
