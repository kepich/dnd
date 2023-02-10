from PyQt6.QtCore import QTimer, QRect, Qt, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSlider, QGridLayout, QHBoxLayout

from rightPanel.WeatherWidget import WeatherWidget
from utils.WeatherTimeUtils import TimeDuration, TimeDurationDict, TimeDurationInvertedDict, MAX_DARKNESS


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
        self.drawAllTime(self.time)

    def setTimeSpeed(self):
        self.timeSpeed = TimeDurationDict[self.timeDurationSlider.value()]

    def startTime(self):
        self.timer.start(1000)

    def endTime(self):
        self.timer.stop()

    def showTime(self):
        dt = self.time
        self.updateTime(self.timeSpeed.value)
        self.drawAllTime(dt)
        self.parent().parent().canvas.networkProxy.weatherSend(self.getCurrentTimeData())

    def drawAllTime(self, oldTime):
        h = int(self.time / TimeDuration.S_2_H.value)
        m = int((self.time % TimeDuration.S_2_H.value) / TimeDuration.S_2_M.value)
        s = int(self.time % TimeDuration.S_2_M.value)
        timeString = f"{f'0{h}' if h < 10 else f'{h}'}:" \
                     f"{f'0{m}' if m < 10 else f'{m}'}:" \
                     f"{f'0{s}' if s < 10 else f'{s}'}"

        self.drawClock(timeString, f"Day {self.days}")
        self.nightRedraw(h, oldTime)

    def nightRedraw(self, h, oldTime):
        oh = int(oldTime / TimeDuration.S_2_H.value)
        if h != oh:
            if 22 >= h >= 18:
                self.parent().parent().canvas.darknessValue = MAX_DARKNESS / 4 * (h - 18)
                self.parent().parent().canvas.redraw()
            elif 6 <= h <= 10:
                self.parent().parent().canvas.darknessValue = MAX_DARKNESS / 4 * (10 - h)
                self.parent().parent().canvas.redraw()
            elif 18 > h > 10:
                self.parent().parent().canvas.darknessValue = 0
            else:
                self.parent().parent().canvas.darknessValue = MAX_DARKNESS

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
        self.timeDurationSlider.setRange(0, 7)
        self.timeDurationSlider.setTickPosition(QSlider.TickPosition.TicksAbove)

        layout = QGridLayout()
        layout.addWidget(self.timeDurationSlider, 0, 0, 1, 8)
        layout.addWidget(l0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(l1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(l2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(l3, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(l4, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(l5, 1, 5, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(l6, 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(l7, 1, 7, alignment=Qt.AlignmentFlag.AlignCenter)

        return layout

    def getCurrentTimeData(self) -> dict:
        return {
            "time": self.time,
            "days": self.days,
            "timeSpeed": self.timeSpeed,
            "weather": self.weatherWidget.getTempWeather()
        }

    def setCurrentTimeData(self, data: dict):
        dt = self.time
        self.time = data["time"]
        self.days = data["days"]
        self.timeSpeed = data["timeSpeed"]
        self.timeDurationSlider.setValue(TimeDurationInvertedDict[self.timeSpeed])
        self.weatherWidget.setTempWeather(data["weather"])
        self.weatherWidget.drawWeather()
        self.drawAllTime(dt)
