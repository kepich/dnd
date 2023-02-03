from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from Message import Message


# # External calls handlers
# receivedSignal              = pyqtSignal(Message)
# connectionEstablishedSignal = pyqtSignal()
# playerJoinSignal            = pyqtSignal(str)
# playerLeaveSignal           = pyqtSignal(str)
# chatSignal                  = pyqtSignal(list)
#
# API = {
#     "update": lambda msg: receivedSignal.emit(Message.fromBytes(msg)),
#     "connect": lambda: connectionEstablishedSignal.emit(),
#     "player_join": lambda msg: playerJoinSignal.emit(msg),
#     "player_leave": lambda msg: playerLeaveSignal.emit(msg),
#     "chat_msg": lambda msg: chatSignal.emit(msg)
# }
#
# # Internal signals
# connectionRejectedSignal = pyqtSignal()

class ApiSignals(QWidget):
    # External signals
    receivedSignal = pyqtSignal(Message)
    connectionEstablishedSignal = pyqtSignal()
    playerJoinSignal = pyqtSignal(str)
    playerLeaveSignal = pyqtSignal(str)
    chatSignal = pyqtSignal(list)

    # Internal signals
    connectionRejectedSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.API = {
            "update": lambda msg: self.receivedSignal.emit(Message.fromBytes(msg)),
            "connect": lambda: self.connectionEstablishedSignal.emit(),
            "player_join": lambda msg: self.playerJoinSignal.emit(msg),
            "player_leave": lambda msg: self.playerLeaveSignal.emit(msg),
            "chat_msg": lambda msg: self.chatSignal.emit(msg)
        }

    def __new__(cls):
        if not hasattr(cls, 'singleton'):
            cls.singleton = super(ApiSignals, cls).__new__(cls)
        return cls.singleton
