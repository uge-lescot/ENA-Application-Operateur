import logging as log
import sys
if r"C:\Users\ena\AppData\Local\Programs\Python\Python39" not in sys.path :
    sys.path.append(r"C:\Users\ena\AppData\Local\Programs\Python\Python39")


from sys import argv
from pathlib import Path

from cadisp import Dashboard
from PyQt5 import QtWidgets
 ############################################### main_server est le 1er script à lancer, il lance tout #####################
if __name__ == '__main__':
    log_file = Path(__file__).parent.resolve() / "main_server.log"
    log.basicConfig(filename=log_file, format="%(asctime)-15s [%(levelname)-8s]: %(message)s", level=log.DEBUG)
    app = QtWidgets.QApplication(argv)
    launcher = Dashboard()
    app.exec_()
