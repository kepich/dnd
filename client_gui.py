import sys
import traceback

from PyQt6.QtWidgets import QApplication

from ClientWindow import ClientWindow


def run():
    app = QApplication([])

    try:
        window = ClientWindow()
        window.show()
    except:
        traceback.print_exc()

    sys.exit(app.exec())


if __name__ == '__main__':
    run()
