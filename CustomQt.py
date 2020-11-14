import PyQt5
from PyQt5.QtWidgets import *
from ProcessMemoryReaders import Spelunky2MemReader

class MainWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def attachToSpelunky(self):
        self.spelunkyReader = Spelunky2MemReader()