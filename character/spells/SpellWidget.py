from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton


class CastWidget(QWidget):
    addSignal = pyqtSignal(dict)
    removeSignal = pyqtSignal(dict)

    def __init__(self, castInfo, parent=None, isAdded=False):
        super().__init__(parent)

        self.castInfo = castInfo
        self.isAdded = False
        self.addButton = QPushButton()

        if isAdded:
            self.addButton.setText("Remove")
            self.addButton.clicked.connect(lambda: self.removeSignal.emit(self.castInfo))
        else:
            self.addButton.setText("Add")
            self.addButton.clicked.connect(lambda: self.addSignal.emit(self.castInfo))

        grid = QGridLayout()
        grid.setColumnStretch(5, 1)
        grid.addWidget(QLabel(f'<b>{castInfo["name"]}</b>'), 0, 0,
                       alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(QLabel(f'<i>{castInfo["level"]}</i>'), 0, 1,
                       alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.addButton, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        castTime = QLabel(f"<b>Casting time:</b> {castInfo['castingTime']}")
        castTime.setMinimumWidth(200)
        castTime.setWordWrap(True)
        grid.addWidget(castTime, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(QLabel(f"<b>Range:</b> {castInfo['range']}"), 1, 1,
                       alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        grid.addWidget(QLabel(f"<b>Components:</b> <i>{castInfo['components']}</i>"), 2, 0,
                       alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(QLabel(f"<b>Duration:</b> <i>{castInfo['duration']}</i>"), 2, 1,
                       alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        if "need" in castInfo.keys():
            label = QLabel(f"<b>Need:</b> <i>{castInfo['need']}</i>")
            label.setWordWrap(True)
            grid.addWidget(label, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        desc = QLabel(f"<b>Description:</b> {castInfo['description']}")
        desc.setWordWrap(True)
        grid.addWidget(desc, 4, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.setRowStretch(5, 1)

        self.setLayout(grid)
