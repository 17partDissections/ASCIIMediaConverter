import sys
from PyQt5.QtWidgets import *
from MainWindow import *
if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow()
    sys.exit(app.exec())