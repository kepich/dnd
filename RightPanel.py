from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class RightPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.button1 = QPushButton()
        self.button1.setText("ALLAHU AKBAR")
        self.button1.setFixedWidth(100)
        self.button1.setFixedHeight(100)

        self.setFixedWidth(300)

        vertical_layout.addWidget(self.button1)
        vertical_layout.addStretch(1)

        self.setLayout(vertical_layout)
