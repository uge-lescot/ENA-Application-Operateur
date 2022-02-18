from PyQt5 import QtCore


class CadispServer(QtCore.QThread):
    sig_mode = QtCore.pyqtSignal(str)
    sig_shutdown = QtCore.pyqtSignal()

    _MESSAGES = ["active", "tor", "none",
                 "manual", "auto_available", "autonomous",
                 "end_zone", "critical", "safety_stop"]

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def process_message(self, data: dict):
        if data["action"] in self._MESSAGES:
            self.sig_mode.emit(data["action"])
        elif data["action"] == "shutdown":
            self.sig_shutdown.emit()
