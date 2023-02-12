from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton


class CastWidget(QWidget):
    def __init__(self, castInfo, parent=None):
        super().__init__(parent)

        self.castInfo = castInfo
        self.addButton = QPushButton("Add")

        grid = QGridLayout()
        grid.setColumnStretch(5, 1)
        grid.addWidget(QLabel(f'<b>{castInfo["name"]}</b>'), 0, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(QLabel(f'<i>{castInfo["level"]}</i>'), 0, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.addButton, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        grid.addWidget(QLabel(f"<b>Casting time:</b> {castInfo['castingTime']}"), 1, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(QLabel(f"<b>Range:</b> {castInfo['range']}"), 1, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        grid.addWidget(QLabel(f"<b>Components:</b> <i>{castInfo['components']}</i>"), 2, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(QLabel(f"<b>Duration:</b> <i>{castInfo['duration']}</i>"), 2, 1, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        if "need" in castInfo.keys():
            label = QLabel(f"<b>Need:</b> <i>{castInfo['duration']}</i>")
            label.setWordWrap(True)
            grid.addWidget(label, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        desc = QLabel(f"<b>Description:</b> {castInfo['description']}")
        desc.setWordWrap(True)
        grid.addWidget(desc, 4, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.setRowStretch(5, 1)

        self.setLayout(grid)
