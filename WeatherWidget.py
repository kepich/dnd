import random
import time
from enum import Enum

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class CloudType(Enum):
    CLEAR = 0
    SMALL_CLOUDS = 1
    CLOUDS = 2
    SMALL_RAIN = 3
    RAIN = 4
    THUNDER = 5


cloudTypeDict = {
    CloudType.CLEAR: "Clear",
    CloudType.SMALL_CLOUDS: "Small clouds",
    CloudType.CLOUDS: "Clouds",
    CloudType.SMALL_RAIN: "Small rain",
    CloudType.RAIN: "Rain",
    CloudType.THUNDER: "Thunder",
}

cloudTypeValuesDict = {
    0: CloudType.CLEAR,
    1: CloudType.SMALL_CLOUDS,
    2: CloudType.CLOUDS,
    3: CloudType.SMALL_RAIN,
    4: CloudType.RAIN,
    5: CloudType.THUNDER
}


class WindDirection(Enum):
    S = 0
    SE = 1
    E = 2
    NE = 3
    N = 4
    NW = 5
    W = 6
    SW = 7

windDirectionDict = {
    0: WindDirection.S,
    1: WindDirection.SE,
    2: WindDirection.E,
    3: WindDirection.NE,
    4: WindDirection.N,
    5: WindDirection.NW,
    6: WindDirection.W,
    7: WindDirection.SW
}


class WeatherWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.windPower = 0
        self.windDirection = WindDirection.S
        self.clouds = CloudType.CLEAR

        self.vLayout = QVBoxLayout()
        self.cloudsLabel = QLabel(self.getTempClouds())
        self.windLabel = QLabel(self.getTempWind())
        self.vLayout.addWidget(self.cloudsLabel)
        self.vLayout.addWidget(self.windLabel)

        self.setLayout(self.vLayout)
        self.rndSeed = time.time()
        self.rnd = random.Random(self.rndSeed)

    def getTempClouds(self):
        return f"Sky: {cloudTypeDict[self.clouds]}"

    def getTempWind(self):
        return f"Wind: {self.windDirection.name}, {self.windPower} m/s"

    def updateWeather(self):
        windMultiplier = 2
        if self.windPower > 25:
            self.windPower = abs(self.windPower + random.choice([-1, 0, 0, 0, 0, 0]) * windMultiplier)
        elif self.windPower == 0:
            self.windPower = abs(self.windPower + random.choice([0, 0, 0, 0, 1]) * windMultiplier)
        else:
            self.windPower = abs(self.windPower + random.choice([-1, 0, 0, 1]) * windMultiplier)

        newWindDirection = self.windDirection.value + random.choice([-1, 0, 0, 1])
        if newWindDirection > 7:
            newWindDirection = 0
        elif newWindDirection < 0:
            newWindDirection = 7
        self.windDirection = windDirectionDict[newWindDirection]

        if self.clouds.value == 0:
            newClouds = self.clouds.value + random.choice([0, 0, 1])
        elif self.clouds.value == 5:
            newClouds = self.clouds.value + random.choice([0, 0, -1])
        else:
            newClouds = self.clouds.value + random.choice([1, 0, -1])

        self.clouds = cloudTypeValuesDict[newClouds]

        self.drawWeather()

    def getTempWeather(self) -> dict:
        return {
             "windPower": self.windPower,
             "windDirection": self.windDirection,
             "clouds": self.clouds
        }

    def setTempWeather(self, weatherData: dict) -> None:
        self.windPower = weatherData["windPower"]
        self.windDirection = weatherData["windDirection"]
        self.clouds = weatherData["clouds"]

    def drawWeather(self):
        self.cloudsLabel.setText(self.getTempClouds())
        self.windLabel.setText(self.getTempWind())
