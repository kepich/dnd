import pickle
import traceback

import socketio
from PyQt6.QtCore import QThread, pyqtSignal

from Message import Message


class SocketClient(QThread):
    receivedSignal              = pyqtSignal(Message)
    connectionEstablishedSignal = pyqtSignal()
    connectionRejectedSignal    = pyqtSignal()
    playerJoinSignal            = pyqtSignal(str)
    playerLeaveSignal           = pyqtSignal(str)
    chatSignal                  = pyqtSignal(list)
    needFirstLoadSignal         = pyqtSignal()
    firstLoadSignal             = pyqtSignal(list)
    weatherTimeSignal           = pyqtSignal(dict)
    masterFirstLoadSignal       = pyqtSignal()
    caveDarknessSignal          = pyqtSignal(bool)

    sio = socketio.Client()

    def __init__(self, ip, port, nickname):
        super().__init__()
        self.queue = []
        self.ip = ip
        self.port = port
        self.nickname = nickname
        self.headers = {"nickname": nickname}

        self.sio.on("connect", self.connectionEstablishedSignal.emit)
        self.sio.on("update", lambda msg: self.receivedSignal.emit(pickle.loads(msg)))
        self.sio.on("player_join", self.playerJoinSignal.emit)
        self.sio.on("player_leave", self.playerLeaveSignal.emit)
        self.sio.on("chat_msg", self.chatSignal.emit)
        self.sio.on("need_first_load", self.needFirstLoadSignal.emit)
        self.sio.on("first_load", lambda msg: self.firstLoadSignal.emit(pickle.loads(msg)))
        self.sio.on("weather_time", lambda msg: self.weatherTimeSignal.emit(pickle.loads(msg)))
        self.sio.on("master_first_load", self.masterFirstLoadSignal.emit)
        self.sio.on("cave_darkness", lambda msg: self.caveDarknessSignal.emit(pickle.loads(msg)))

        self.isActive = True

    def run(self):
        try:
            self.sio.connect(f'http://{self.ip}:{self.port}', headers=self.headers)

            while self.isActive:
                if len(self.queue) > 0:
                    msg = self.queue[0]
                    self.queue.remove(msg)
                    self.sio.emit('broadcast_msg', pickle.dumps(msg))
        except:
            traceback.print_exc()
            self.connectionRejectedSignal.emit()

    def closeConnection(self):
        self.sio.disconnect()
        self.isActive = False

    def sendChatMessage(self, msg: str):
        return self.sio.emit("chat_msg", msg)

    def sendFirstLoad(self, msg: list[dict]):
        return self.sio.emit("first_load", pickle.dumps(msg))

    def sendWeather(self, objects):
        return self.sio.emit("weather_time", pickle.dumps(objects))

    def caveSend(self, value):
        return self.sio.emit("cave_darkness", pickle.dumps(value))