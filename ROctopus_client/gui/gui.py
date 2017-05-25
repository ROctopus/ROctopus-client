# import sys
# import time
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ..client import client
from .mainwindow import *
from .gui_settings import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.InitUi()
        self.settings = QtCore.QSettings('ROctopus', 'ROctopus')

    def InitUi(self):
        self.ui.actionSettings.triggered.connect(self.InitSettings)
        self.ui.connect_button.clicked.connect(self.connect_to_server)
        # self.ui.run_button.clicked.connect(self.)
        self.ui.quit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.show()
        # QtCore.QCoreApplication.instance().quit()

    def InitSettings(self):
        self.dialog = SettingsDialog()
        if self.dialog.exec_(): # Modal window. Use .show() for modeless.
            values = self.dialog.getValues()
            print(values)
            for (key, value) in values.items():
                self.settings.setValue(key, value)
        # TODO: Check for errors.

    def get_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        # TODO: Find a way to write this to the line edit.

    def update_statusbar(self, text):
        self.statusBar().showMessage(text)

    def get_task(self):
        # Deprecated.
        self.statusBar().showMessage('Getting task from: ' + self.ui.ip_entry.text() + ':' + self.ui.port_entry.text())
        self.task = client.Task(self.ui.ip_entry.text(), self.ui.port_entry.text()) # Make ip and port class attributes?
        self.ui.task_info.setText(str(self.task.id))
        self.statusBar().showMessage('Task arrived!')

    def start_task(self):
        # Deprecated.
        self.statusBar().showMessage('Task starts! Window will hang :(')
        self.task.run()
        self.statusBar().showMessage('Task finished!')
        self.task.send_results(self.settings.value('ip_entry', type=str), self.settings.value('port_entry', type=int))
        self.statusBar().showMessage('Task output sent back!')

    def connect_to_server(self):
        return 1


    def create_thread(self):
        self.workerthread = QtCore.QThread()
        self.workerthread.start()

    def start_thread(self):
        try:
            self.worker = threadWorker(self.task, self.settings.value('ip_entry', type=str), self.settings.value('port_entry', type=int))
            self.worker.start.connect(self.worker.run)
            self.worker.start.connect(self.update_statusbar)
            self.worker.finished.connect(self.update_statusbar)

            self.worker.moveToThread(self.workerthread)
            self.worker.start.emit('Task starts!')
        except AttributeError:
            self.create_thread()

            self.worker = threadWorker(self.task, self.ui.ip_entry.text(), self.ui.port_entry.text())
            self.worker.start.connect(self.worker.run)
            self.worker.start.connect(self.update_statusbar)
            self.worker.finished.connect(self.update_statusbar)

            self.worker.moveToThread(self.workerthread)
            self.worker.start.emit('Task starts!')


    def process_thread(self):
        self.statusBar().showMessage('Task finished and output sent back!')

class threadWorker(QtCore.QObject):
    def __init__(self, task, ip, port):
        super().__init__()
        self.task = task
        self.ip = ip
        self.port = port

    start = pyqtSignal(str)
    finished = pyqtSignal(str)
    @pyqtSlot()
    def run(self):
        print('Worker started!')
        self.task.run()
        self.finished.emit('Task finished!')
