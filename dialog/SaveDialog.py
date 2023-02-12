from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton


class SaveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Save")

        self.vLayout = QVBoxLayout()
        self.saveNameTextBox = QLineEdit()
        self.vLayout.addWidget(self.saveNameTextBox)

        self.hLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.saveButton.pressed.connect(self.accept)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.pressed.connect(self.reject)
        self.hLayout.addWidget(self.saveButton)
        self.hLayout.addWidget(self.cancelButton)

        self.vLayout.addLayout(self.hLayout)

        self.setLayout(self.vLayout)
