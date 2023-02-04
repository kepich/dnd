from enum import Enum

from PyQt6.QtCore import QTimer, QRect, Qt, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class TimeDuration(Enum):
    S_2_S = 1
    S_2_M = 60
    S_2_10M = 600
    S_2_30M = 1800
    S_2_H = 3600
    S_2_12H = 43200
    S_2_D = 86400
    S_2_W = 604800


class TimeWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timerPixmap = QPixmap("resources/timer.png")
        self.clockPixmap = QPixmap("resources/clock.png")

        self.verticalLayout = QVBoxLayout()
        self.clock = QLabel("")
        pixmap = QPixmap(100, 100)
        pixmap.fill(Qt.GlobalColor.transparent)
        self.clock.setPixmap(pixmap)
        self.verticalLayout.addWidget(self.clock)

        self.timeLabel = QLabel("")
        self.verticalLayout.addWidget(self.timeLabel)

        self.setLayout(self.verticalLayout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)

        self.time = 0
        self.angle = 0
        self.timeSpeed = TimeDuration.S_2_30M
        self.showTime()

    def showTime(self):
        self.updateTime(self.timeSpeed.value)
        h = int(self.time / TimeDuration.S_2_H.value)
        m = int((self.time % TimeDuration.S_2_H.value) / TimeDuration.S_2_M.value)
        s = int(self.time % TimeDuration.S_2_M.value)
        timeString = f"{f'0{h}' if h < 10 else f'{h}'}:"\
                     f"{f'0{m}' if m < 10 else f'{m}'}:"\
                     f"{f'0{s}' if s < 10 else f'{s}'}"

        self.drawTime(timeString)

    def startTime(self):
        self.timer.start(1000)

    def endTime(self):
        self.timer.stop()

    def updateTimePeriod(self, duration: TimeDuration):
        self.timeSpeed = duration

    def updateTime(self, value):
        self.time = (self.time + value) % TimeDuration.S_2_D.value
        self.angle = int(self.time / 240)

    def syncTime(self, tempTime, duration: TimeDuration):
        self.timeSpeed = duration
        self.time = tempTime

    def drawTime(self, timeString):
        pixmap = self.clock.pixmap()
        painter = QPainter(pixmap)

        painter.begin(pixmap)

        size = QRect(5, 5, self.clock.pixmap().width() - 10, self.clock.pixmap().height() - 10)
        transform = QTransform().rotate(self.angle)
        rotated = self.timerPixmap.transformed(transform)
        painter.drawPixmap(size, rotated.copy((rotated.width() - self.timerPixmap.width()) / 2,
                                              (rotated.height() - self.timerPixmap.height()) / 2,
                                              self.timerPixmap.width(), self.timerPixmap.height()))

        size = QRect(0, 0, self.clock.pixmap().width(), self.clock.pixmap().height())
        painter.drawPixmap(size, self.clockPixmap)
        point = QPoint(30, 70)
        painter.drawText(point, timeString)

        self.clock.setPixmap(pixmap)

        painter.end()