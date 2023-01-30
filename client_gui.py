import sys

from PyQt6.QtWidgets import QApplication

from ClientWindow import ClientWindow


def run():
    app = QApplication([])

    window = ClientWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
