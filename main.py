import sys
import subprocess
import threading
import tempfile
import base64
import requests
import os.path

from PyQt5 import QtCore, QtGui, QtWidgets
from socketIO_client import SocketIO, BaseNamespace

import client
import gui

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = gui.MainWindow()
    sys.exit(app.exec_())
