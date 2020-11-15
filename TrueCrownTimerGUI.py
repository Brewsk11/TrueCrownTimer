import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

if __name__ == '__main__':

    app = QApplication(sys.argv)

    mwin = QMainWindow()
    uic.loadUi('./GUIDefinition.ui', mwin)
    mwin.show()

    app.exec_()
