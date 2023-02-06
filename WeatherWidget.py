import random
import time

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from WeatherTimeUtils import extraWindDecreaseValues, noWindIncreaseValues, windChangeValues, \
    windDirectionChangingValues, noCloudsIncreaseValues, extraCloudsDecreaseValues, cloudsChangeValues, WindDirection, \
    CloudType, CloudTypeNameDict, WindDirectionDict, CloudTypeDict


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
        return f"Sky: {CloudTypeNameDict[self.clouds]}"

    def getTempWind(self):
        return f"Wind: {self.windDirection.name}, {self.windPower} m/s"

    def updateWeather(self):
        if self.windPower > 25:
            self.windPower = abs(self.windPower + random.choice(extraWindDecreaseValues))
        elif self.windPower == 0:
            self.windPower = abs(self.windPower + random.choice(noWindIncreaseValues))
        else:
            self.windPower = abs(self.windPower + random.choice(windChangeValues))

        newWindDirection = self.windDirection.value + random.choice(windDirectionChangingValues)
        if newWindDirection > 7:
            newWindDirection = 0
        elif newWindDirection < 0:
            newWindDirection = 7
        self.windDirection = WindDirectionDict[newWindDirection]

        if self.clouds.value == 0:
            self.clouds = CloudTypeDict[self.clouds.value + random.choice(noCloudsIncreaseValues)]
        elif self.clouds.value == 5:
            self.clouds = CloudTypeDict[self.clouds.value + random.choice(extraCloudsDecreaseValues)]
        else:
            self.clouds = CloudTypeDict[self.clouds.value + random.choice(cloudsChangeValues)]

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
