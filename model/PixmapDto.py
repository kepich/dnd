from PyQt6.QtCore import QByteArray, QDataStream, QIODevice
from PyQt6.QtGui import QPixmap


class PixmapDto:
    def __init__(self, pixmap):
        self.pixmap = pixmap

    def __getstate__(self):
        qbyte_array = QByteArray()
        stream = QDataStream(qbyte_array, QIODevice.OpenModeFlag.WriteOnly)
        stream << self.pixmap
        return qbyte_array

    def __setstate__(self, buffer):
        self.pixmap = QPixmap()
        stream = QDataStream(buffer, QIODevice.OpenModeFlag.ReadOnly)
        stream >> self.pixmap
