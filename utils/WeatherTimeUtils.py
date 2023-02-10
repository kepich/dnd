from enum import Enum


class TimeDuration(Enum):
    S_2_S = 1
    S_2_M = 60
    S_2_10M = 600
    S_2_30M = 1800
    S_2_H = 3600
    S_2_12H = 43200
    S_2_D = 86400
    S_2_W = 604800


TimeDurationDict = {
    0: TimeDuration.S_2_S,
    1: TimeDuration.S_2_M,
    2: TimeDuration.S_2_10M,
    3: TimeDuration.S_2_30M,
    4: TimeDuration.S_2_H,
    5: TimeDuration.S_2_12H,
    6: TimeDuration.S_2_D,
    7: TimeDuration.S_2_W,
}

TimeDurationInvertedDict = {v: k for k, v in TimeDurationDict.items()}


class CloudType(Enum):
    CLEAR = 0
    SMALL_CLOUDS = 1
    CLOUDS = 2
    SMALL_RAIN = 3
    RAIN = 4
    THUNDER = 5


CloudTypeNameDict = {
    CloudType.CLEAR: "Clear",
    CloudType.SMALL_CLOUDS: "Small clouds",
    CloudType.CLOUDS: "Clouds",
    CloudType.SMALL_RAIN: "Small rain",
    CloudType.RAIN: "Rain",
    CloudType.THUNDER: "Thunder",
}

CloudTypeDict = {
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


WindDirectionDict = {
    0: WindDirection.S,
    1: WindDirection.SE,
    2: WindDirection.E,
    3: WindDirection.NE,
    4: WindDirection.N,
    5: WindDirection.NW,
    6: WindDirection.W,
    7: WindDirection.SW
}

MAX_DARKNESS = 0.90

extraWindDecreaseValues = [-1, 0, 0, 0, 0, 0]
noWindIncreaseValues = [0, 0, 0, 0, 1]
windChangeValues = [-1, -1, 0, 1]
windDirectionChangingValues = [-1, 0, 0, 1]

noCloudsIncreaseValues = [0, 0, 1]
extraCloudsDecreaseValues = [0, 0, -1]
cloudsChangeValues = [1, 0, -1]
