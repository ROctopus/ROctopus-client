'''rocto-client main script.'''

import sys
import logging
import tempfile

from PyQt5 import QtCore, QtWidgets, QtGui
from rocto_client.Qt.ui.importer import MainWindow


def main():
    # create tempfile for logging
    tf = tempfile.NamedTemporaryFile()
    logging.basicConfig(filename = tf.name+".log", level = logging.DEBUG)
    print("Logging to: " + tf.name)

    # Setup the app with high-dpi scaling on windows
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    # start the window
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
