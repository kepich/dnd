from enum import Enum

from PyQt6.QtCore import QTimer, QRect, Qt, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSlider, QGridLayout, QHBoxLayout, QPushButton

from WeatherWidget import WeatherWidget


class TimeDuration(Enum):
    S_2_S = 1
    S_2_M = 60
    S_2_10M = 600
    S_2_30M = 1800
    S_2_H = 3600
    S_2_12H = 43200
    S_2_D = 86400
    S_2_W = 604800


durationDict = {
    0: TimeDuration.S_2_S,
    1: TimeDuration.S_2_M,
    2: TimeDuration.S_2_10M,
    3: TimeDuration.S_2_30M,
    4: TimeDuration.S_2_H,
    5: TimeDuration.S_2_12H,
    6: TimeDuration.S_2_D,
    7: TimeDuration.S_2_W,
}

invDurationDict = {v: k for k, v in durationDict.items()}


class TimeWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timerPixmap = QPixmap("resources/timer.png")
        self.clockPixmap = QPixmap("resources/clock.png")

        self.verticalLayout = QVBoxLayout()
        self.clockHLayout = QHBoxLayout()
        self.clock = QLabel("")
        pixmap = QPixmap(100, 100)
        pixmap.fill(Qt.GlobalColor.transparent)
        self.clock.setPixmap(pixmap)
        self.clockHLayout.addWidget(self.clock)
        self.weatherWidget = WeatherWidget()
        self.clockHLayout.addWidget(self.weatherWidget)

        self.verticalLayout.addLayout(self.clockHLayout)

        self.hLayout = QHBoxLayout()

        vLayout = QVBoxLayout()
        self.hLayout.addLayout(vLayout)
        self.morningButton = QPushButton("Morning")
        self.morningButton.pressed.connect(lambda: self.setTime(25200))
        self.midnightButton = QPushButton("Midnight")
        self.midnightButton.pressed.connect(lambda: self.setTime(TimeDuration.S_2_D.value))
        vLayout.addWidget(self.morningButton)
        vLayout.addWidget(self.midnightButton)

        self.sliderLayout = self.addSlider()
        self.timeDurationSlider.sliderReleased.connect(self.setTimeSpeed)

        self.hLayout.addLayout(self.sliderLayout)
        self.verticalLayout.addLayout(self.hLayout)

        self.setLayout(self.verticalLayout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)

        self.time = 0
        self.days = 0
        self.timeSpeed = TimeDuration.S_2_S
        self.drawAllTime()

    def setTime(self, time: int):
        self.time = time

    def setTimeSpeed(self):
        self.timeSpeed = durationDict[self.timeDurationSlider.value()]

    def startTime(self):
        self.timer.start(1000)

    def endTime(self):
        self.timer.stop()

    def showTime(self):
        self.updateTime(self.timeSpeed.value)
        self.drawAllTime()
        self.parent().parent().canvas.networkProxy.weatherSend(self.getCurrentTimeData())

    def drawAllTime(self):
        h = int(self.time / TimeDuration.S_2_H.value)
        m = int((self.time % TimeDuration.S_2_H.value) / TimeDuration.S_2_M.value)
        s = int(self.time % TimeDuration.S_2_M.value)
        timeString = f"{f'0{h}' if h < 10 else f'{h}'}:" \
                     f"{f'0{m}' if m < 10 else f'{m}'}:" \
                     f"{f'0{s}' if s < 10 else f'{s}'}"

        self.drawClock(timeString, f"Day {self.days}")

    def updateTime(self, value):
        self.days = self.days + int((self.time + value) / TimeDuration.S_2_D.value)
        dh = int((self.time + value) / TimeDuration.S_2_H.value) - int(self.time / TimeDuration.S_2_H.value)
        self.time = (self.time + value) % TimeDuration.S_2_D.value

        for _ in range(dh):
            self.weatherWidget.updateWeather()

    def drawClock(self, timeString, dayString):
        pixmap = self.clock.pixmap()
        painter = QPainter(pixmap)

        painter.begin(pixmap)

        size = QRect(5, 5, self.clock.pixmap().width() - 10, self.clock.pixmap().height() - 10)
        transform = QTransform().rotate(int(self.time / 240) + 180)
        rotated = self.timerPixmap.transformed(transform)
        painter.drawPixmap(size, rotated.copy((rotated.width() - self.timerPixmap.width()) / 2,
                                              (rotated.height() - self.timerPixmap.height()) / 2,
                                              self.timerPixmap.width(), self.timerPixmap.height()))

        size = QRect(0, 0, self.clock.pixmap().width(), self.clock.pixmap().height())
        painter.drawPixmap(size, self.clockPixmap)
        point = QPoint(30, 65)
        painter.drawText(point, timeString)
        point = QPoint(30, 80)
        painter.drawText(point, dayString)

        self.clock.setPixmap(pixmap)

        painter.end()

    def addSlider(self):
        l0 = QLabel("S")
        l1 = QLabel("M")
        l2 = QLabel("10M")
        l3 = QLabel("30M")
        l4 = QLabel("H")
        l5 = QLabel("12H")
        l6 = QLabel("D")
        l7 = QLabel("W")

        self.timeDurationSlider = QSlider(Qt.Orientation.Horizontal)
        self.timeDurationSlider.setFixedWidth(200)
        self.timeDurationSlider.setRange(0, 7)

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timeDurationSlider, 0, 0, 1, 8)
        layout.addWidget(l0, 1, 0, 1, 1)
        layout.addWidget(l1, 1, 1, 1, 1)
        layout.addWidget(l2, 1, 2, 1, 1)
        layout.addWidget(l3, 1, 3, 1, 1)
        layout.addWidget(l4, 1, 4, 1, 1)
        layout.addWidget(l5, 1, 5, 1, 1)
        layout.addWidget(l6, 1, 6, 1, 1)
        layout.addWidget(l7, 1, 7, 1, 1)

        return layout

    def getCurrentTimeData(self) -> dict:
        return {
            "time": self.time,
            "days": self.days,
            "timeSpeed": self.timeSpeed,
            "weather": self.weatherWidget.getTempWeather()
        }

    def setCurrentTimeData(self, data: dict):
        self.time = data["time"]
        self.days = data["days"]
        self.timeSpeed = data["timeSpeed"]
        self.timeDurationSlider.setValue(invDurationDict[self.timeSpeed])
        self.weatherWidget.setTempWeather(data["weather"])
        self.weatherWidget.drawWeather()
        self.drawAllTime()
