import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ProcessMemoryReaders import Spelunky2MemReader
import playsound
import threading

class MainWidget(QWidget):

    CROWN_INTERVAL = 22
    EMERGENCY_BAR_AT = 3

    NOTIFY_AT = [5, 2, 1, 0]

    NOTIFICATION_FILE = './notification.mp3'

    # Debug
    MOCK_CONNECTION = False

    levelTimerUpdate = pyqtSignal(str)
    nextTpTimeLeftUpdate = pyqtSignal(str)
    nextTpTimeLeftPercentUpdate = pyqtSignal(int)
    nextTpTimeLeftNotificationPercentUpdate = pyqtSignal(int)

    previousTpTimeUpdate = pyqtSignal(str)
    nextTpTimeUpdate = pyqtSignal(str)
    tpThisLevelUpdate = pyqtSignal(str)
    tpAllUpdate = pyqtSignal(str)

    attachStatusUpdate = pyqtSignal(str)
    trueCrownStatusUpdate = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_timer = QTimer()
        self.update_timer.setInterval(10)
        self.update_timer.timeout.connect(self.timerTick)

        self.trueCrownActive = None

        self.mock_timer = 0

        self.prev_frame_val = -1

        self.notify_table = { x: False for x in self.NOTIFY_AT }

    def attachToSpelunky(self):
        message = ""
        try:
            if not self.MOCK_CONNECTION:
                self.spelunkyReader = Spelunky2MemReader()
            message = "Attached"
            self.setTrueCrownActive(False)
            self.update_timer.start()
        except Exception as e:
            message = f"Error: {e}"

        self.attachStatusUpdate.emit(message)
    
    def dissectFltSeconds(self, value: float):
        milliseconds = int((value % 1) * 1000) 
        centiseconds = int((value % 1) * 100) 
        deciseconds = int((value % 1) * 10)
        seconds = int(value) % 60
        minutes = int(value) // 60
        return minutes, seconds, deciseconds, centiseconds, milliseconds

    def parseLevelTime(self, value):
        m, s, ds, _, _ = self.dissectFltSeconds(value)

        after_teleport = value % self.CROWN_INTERVAL
        until_teleport = self.CROWN_INTERVAL - after_teleport
        until_teleport_permill = int(after_teleport / self.CROWN_INTERVAL * 1000)

        until_teleport_permill_notification = 0
        if until_teleport < self.EMERGENCY_BAR_AT:
            until_teleport_permill_notification = int((self.EMERGENCY_BAR_AT - until_teleport) / self.EMERGENCY_BAR_AT * 1000)

        self.levelTimerUpdate.emit("{0:01d}:{1:02d}.{2:01d}".format(m, s, ds))

        if self.trueCrownActive:

            self.nextTpTimeLeftUpdate.emit("{:.2f}".format(until_teleport))
            self.nextTpTimeLeftPercentUpdate.emit(until_teleport_permill)
            self.nextTpTimeLeftNotificationPercentUpdate.emit(until_teleport_permill_notification)
            
            tp_prev = 0
            tp_next = self.CROWN_INTERVAL * ((value + self.CROWN_INTERVAL) // self.CROWN_INTERVAL)
            if value >= self.CROWN_INTERVAL:
                tp_prev = self.CROWN_INTERVAL * (value // self.CROWN_INTERVAL)
            
            mn, sn, _, _, _ = self.dissectFltSeconds(tp_next)
            mp, sp, _, _, _ = self.dissectFltSeconds(tp_prev)

            self.previousTpTimeUpdate.emit("{0:01d}:{1:02d}".format(mp, sp))
            self.nextTpTimeUpdate.emit("{0:01d}:{1:02d}".format(mn, sn))

            self.manageNotification(until_teleport)
            # self.tpThisLevelUpdate.emit()
            # self.tpAllUpdate.emit()

    def manageNotification(self, value):
        value = int(value)
        if value == self.CROWN_INTERVAL - 2:
            for item in self.notify_table:
                self.notify_table[item] = False

        if value not in self.notify_table:
            return

        if not self.notify_table[value]:
            self.playNotification()
            self.notify_table[value] = True


    def playNotification(self):
        threading.Thread(target=lambda: playsound.playsound(self.NOTIFICATION_FILE)).start()

    def timerTick(self):

        if self.MOCK_CONNECTION:
            self.mock_timer += 0.01
            self.parseLevelTime(self.mock_timer)
        else:
            try:
                self.parseLevelTime(self.spelunkyReader.readLevelTimer())
            except RuntimeError as e:
                self.attachStatusUpdate.emit("Connection lost, reattach")
                self.update_timer.stop()


    def toggleTrueCrownActive(self):
        self.setTrueCrownActive(not self.trueCrownActive)

    def setTrueCrownActive(self, value):
        pbToggleTrueCrown = self.findChild(QPushButton, 'pbToggleTrueCrown')

        self.trueCrownActive = value
        self.trueCrownStatusUpdate.emit('ENABLED' if value else 'DISABLED')