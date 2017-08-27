'''rocto-client main script.'''

import sys
import logging

from PyQt5 import QtCore, QtWidgets, QtGui
from rocto_client.Qt.ui.importer import MainWindow


def main():
    logging.basicConfig(filename = 'log.log', level = logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
