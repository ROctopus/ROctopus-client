import sys
# import time
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ROctopus_client.client import client
from ROctopus_client.Qt.threads import threadWorker
from ROctopus_client.Qt.mainwindow import Ui_MainWindow
from ROctopus_client.Qt.gui_settings import *
from ROctopus_client.Qt.aboutdialog import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.InitUi()
        self.settings = QtCore.QSettings('ROctopus', 'ROctopus')

    def InitUi(self):
        self.setWindowIcon(QtGui.QIcon('icons/icon.png')) # Relative to runtime directory.
        self.ui.actionSettings.triggered.connect(self.InitSettings)
        self.ui.actionAbout.triggered.connect(self.InitAbout)
        self.ui.connect_button.clicked.connect(self.connect_to_server)
        self.ui.run_button.clicked.connect(self.start_thread)
        self.ui.actionQuit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.ui.quit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.show()

    def InitSettings(self):
        self.settings_dialog = SettingsDialog()
        if self.settings.contains('server_ip') and self.settings.contains('server_ip'):
            self.settings_dialog.ui.ip_entry.setText(self.settings.value('server_ip', type=str))
            self.settings_dialog.ui.port_entry.setText(self.settings.value('port', type=str))

        if self.settings_dialog.exec_(): # Modal window. Use .show() for modeless.
            values = self.settings_dialog.getValues()
            for (key, value) in values.items():
                self.settings.setValue(key, value)

    def InitAbout(self):
        self.about_dialog = AboutDialog()

    def get_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        # TODO: Find a way to write this to the line edit.

    def update_statusbar(self, text):
        self.statusBar().showMessage(text)

    def update_console(self, text):
        self.ui.textEdit.setEnabled(True)
        self.ui.textEdit.append(text)

    def connect_to_server(self):
        # Gets task already at the moment.
        self.ui.connect_status.setEnabled(False)
        print(self.settings.value('server_ip', type=str))
        print(self.settings.value('port', type=int))
        self.task = client.Task(self.settings.value('server_ip', type=str), self.settings.value('port', type=int))
        self.ui.label_3.setEnabled(True)
        self.ui.connect_status.setEnabled(True)
        self.ui.connect_status.setText('Yes!')
        self.ui.groupBox.setEnabled(True)
        self.ui.run_button.setEnabled(True)

    def create_thread(self):
        self.workerthread = QtCore.QThread()
        self.workerthread.start()

    def start_thread(self):
        # EAFP vs LBYL.
        try:
            self.worker = threadWorker(self.task, self.settings.value('server_ip', type=str), self.settings.value('port', type=int))
            self.worker.start.connect(self.worker.run)
            self.worker.start.connect(self.update_console)
            self.worker.finished.connect(self.update_console)
            self.worker.sent.connect(self.update_console)
            self.worker.moveToThread(self.workerthread)
            self.worker.start.emit('Task starts!')
        except AttributeError:
            self.create_thread()
            self.worker = threadWorker(self.task, self.settings.value('server_ip', type=str), self.settings.value('port', type=int))
            self.worker.start.connect(self.worker.run)
            self.worker.start.connect(self.update_console)
            self.worker.finished.connect(self.update_console)
            self.worker.sent.connect(self.update_console)
            self.worker.moveToThread(self.workerthread)
            self.worker.start.emit('Task starts!')

app = QtWidgets.QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())
