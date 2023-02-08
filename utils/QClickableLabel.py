from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel
from PyQt6 import QtGui


class QClickableLabel(QLabel):
    click = pyqtSignal()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.click.emit()