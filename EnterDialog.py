from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QGridLayout, QPushButton


class EnterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Connecting to server")

        self.vLayout = QVBoxLayout()

        self.gridLayout = QGridLayout()

        self.addressLabel = QLabel("Address: ")
        self.addressTextBox = QLineEdit()
        self.portLabel = QLabel("Port: ")
        self.portTextBox = QLineEdit()

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