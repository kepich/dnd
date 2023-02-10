from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel


class QClickableLabel(QLabel):
    click = pyqtSignal()
    textChanged = pyqtSignal(str)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.click.emit()

    def setText(self, a0: str) -> None:
        super().setText(a0)
        self.textChanged.emit(a0)