import traceback
from socket import socket, AF_INET, SOCK_STREAM

from PyQt6.QtCore import QThread, pyqtSignal

from Message import Message


class SocketClient(QThread):
    receivedSignal = pyqtSignal(Message)

    def __init__(self, ip, port):
        super().__init__()
        self.messageQueue = []
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.ip = ip
        self.port = port

    def getMessageQueue(self):
        return self.messageQueue

    def run(self):
        # TODO show connecting screen
        self.clientSocket.connect((self.ip, self.port))
        self.clientSocket.setblocking(False)

        while True:
            # Try to send to server
            if len(self.messageQueue) > 0:
                msg = self.messageQueue[0]
                self.messageQueue.remove(msg)
                print(f"SEND: {msg}")
                self.sendToSocket(msg)
                print(f"SENDED: {msg}")

            received = self.receiveFromSocket()
            if received is not None:
                self.updateObjects(received)

    def sendToSocket(self, msg: Message):
        try:
            self.clientSocket.send(msg.encode())
            print(f"SENDED: {msg}")
        except:
            traceback.print_exc()

    def receiveFromSocket(self):
        try:
            msg = self.clientSocket.recv(1024).decode()
            print(f"RCIEVED: {msg}")
            return msg
        except:
            traceback.print_exc()

    def updateObjects(self, msg):
        try:
            self.receivedSignal.emit(msg)
        except:
            traceback.print_exc()

    def closeConnection(self):
        self.clientSocket.close()
