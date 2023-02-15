from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton


class TakeDamageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Take damage")

        self.vLayout = QVBoxLayout()
        self.damageTextBox = QLineEdit()
        self.damageTextBox.setPlaceholderText("Damage")
        self.damageTextBox.setValidator(QIntValidator())
        self.vLayout.addWidget(self.damageTextBox)

        self.hLayout = QHBoxLayout()
        self.takeDamageButton = QPushButton("Take")
        self.takeDamageButton.pressed.connect(self.accept)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.pressed.connect(self.reject)
        self.hLayout.addWidget(self.takeDamageButton)
        self.hLayout.addWidget(self.cancelButton)

        self.vLayout.addLayout(self.hLayout)

        self.setLayout(self.vLayout)
