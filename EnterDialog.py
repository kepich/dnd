from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QIntValidator
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton


class EnterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Connecting to server")

        self.vLayout = QVBoxLayout()

        self.gridLayout = QGridLayout()

        self.addressLabel = QLabel("Address: ")
        self.addressTextBox = self.createAddressLineEdit()

        self.portLabel = QLabel("Port: ")
        self.portTextBox = self.createPortLineEdit()

        self.gridLayout.addWidget(self.addressLabel, 0, 0)
        self.gridLayout.addWidget(self.addressTextBox, 0, 1)
        self.gridLayout.addWidget(self.portLabel, 1, 0)
        self.gridLayout.addWidget(self.portTextBox, 1, 1)

        self.vLayout.addLayout(self.gridLayout)

        self.hLayout = QHBoxLayout()
        self.connectButton = QPushButton("Connect")
        self.connectButton.pressed.connect(self.accept)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.pressed.connect(self.reject)
        self.hLayout.addWidget(self.connectButton)
        self.hLayout.addWidget(self.cancelButton)

        self.vLayout.addLayout(self.hLayout)

        self.setLayout(self.vLayout)

    def createAddressLineEdit(self):
        lineEdit = QLineEdit()
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegularExpression("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        self.ipValidator = QRegularExpressionValidator(ipRegex, self)
        lineEdit.setValidator(self.ipValidator)
        lineEdit.setText("192.168.0.1")

        return lineEdit

    def createPortLineEdit(self):
        lineEdit = QLineEdit()
        self.portValidator = QIntValidator(0, 65353, self)
        lineEdit.setValidator(self.portValidator)
        lineEdit.setText("50022")

        return lineEdit
