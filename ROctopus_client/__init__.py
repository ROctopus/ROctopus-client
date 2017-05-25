import sys
from PyQt5 import QtWidgets

from .gui import gui

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = gui.MainWindow()
    sys.exit(app.exec_())
