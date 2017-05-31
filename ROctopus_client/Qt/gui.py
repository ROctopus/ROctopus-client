import sys
import psutil
# import time
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ROctopus_client.client import client
from ROctopus_client.client.errors import ServerErr
from ROctopus_client.Qt.threads import threadWorker, threadNetworker
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

    def _create_netwthread(self):
        self.netwthread = QtCore.QThread()
        self.netwthread.start()

    def _create_workthread(self):
        self.workthread = QtCore.QThread()
        self.workthread.start()

    def _handle_conn_status(self, code):
        if code == 1:
            self.ui.conn_status.setEnabled(True) # Change name in .ui
            self.ui.conn_status.setText('Connected!')
            self.ui.connect_button.setText('Disconnect')
            self.ui.runBox.setEnabled(True)
        elif code == 0:
            self.ui.conn_status.setEnabled(False)
            self.ui.conn_status.setText('Disconnected!')

    def _handle_job_recv(self):
        self.ui.run_button.setEnabled(True)
        for i in self.networker.sio.get_namespace().task_list:
            print(i)

    def InitUi(self):
        self.setWindowIcon(QtGui.QIcon('icons/icon.png')) # Relative to runtime directory.
        self.ui.actionSettings.triggered.connect(self.InitSettings)
        self.ui.actionAbout.triggered.connect(self.InitAbout)
        self.ui.connect_button.clicked.connect(self.connect_to_server)
        self.ui.get_task_but.clicked.connect(self.get_job)
        self.ui.run_button.clicked.connect(self.start_thread)
        self.ui.actionQuit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.ui.quit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.show()

    def InitSettings(self):
        self.settings_dialog = SettingsDialog()
        self.settings_dialog.ui.system_ram.setText(str(round(psutil.virtual_memory().total/1024/1024)))
        self.settings_dialog.ui.system_cpu.setText(str(psutil.cpu_count()))

        if self.settings.contains('server_ip') and self.settings.contains('server_ip'):
            self.settings_dialog.ui.ip_entry.setText(self.settings.value('server_ip', type=str))
            self.settings_dialog.ui.port_entry.setText(self.settings.value('port', type=str))

        if self.settings.contains('sys_ram') and self.settings.contains('sys_cores'):
            self.settings_dialog.ui.input_ram.setValue(self.settings.value('sys_ram', type=int))
            self.settings_dialog.ui.input_cpu.setValue(self.settings.value('sys_cores', type=int))

        if self.settings_dialog.exec_(): # Modal window. Use .show() for modeless.
            values = self.settings_dialog.getValues()
            for (key, value) in values.items():
                self.settings.setValue(key, value)

    def InitAbout(self):
        self.about_dialog = AboutDialog()

    def update_statusbar(self, text):
        self.statusBar().showMessage(text)

    def update_console(self, text):
        self.ui.textEdit.setEnabled(True)
        self.ui.textEdit.append(text)

    def connect_to_server(self):
        if self.sender().text() == 'Connect':
            try:
                self.networker = threadNetworker(self.settings.value('server_ip', type = str),\
                self.settings.value('port', type = int))
                self.networker.initconnect.connect(self.networker.socket_connect)
                self.networker.get_job.connect(self.networker.socket_getjob)
                self.networker.conn_status.connect(self._handle_conn_status)
                self.networker.job_recv.connect(self._handle_job_recv)
                self.networker.moveToThread(self.netwthread)
                self.networker.initconnect.emit()
            except AttributeError:
                self._create_netwthread()
                self.networker = threadNetworker(self.settings.value('server_ip', type = str),\
                self.settings.value('port', type = int))
                self.networker.initconnect.connect(self.networker.socket_connect)
                self.networker.get_job.connect(self.networker.socket_getjob)
                self.networker.conn_status.connect(self._handle_conn_status)
                self.networker.job_recv.connect(self._handle_job_recv)
                self.networker.moveToThread(self.netwthread)
                self.networker.initconnect.emit()
        elif self.sender().text() == 'Disconnect':
            pass

    def get_job(self):
        count = self.ui.number_of_tasks.value()
        for i in range(count):
            self.networker.get_job.emit(count)

    def start_thread(self):
        # EAFP vs LBYL.
        try:
            self.worker = threadWorker(self.task, self.settings.value('server_ip', type=str), self.settings.value('port', type=int))
            self.worker.start.connect(self.worker.run)
            self.worker.start.connect(self.update_console)
            self.worker.finished.connect(self.update_console)
            self.worker.sent.connect(self.update_console)
            self.worker.moveToThread(self.workthread)
            self.worker.start.emit('Task starts!')
        except AttributeError:
            self._create_workthread()
            self.worker = threadWorker(self.task, self.settings.value('server_ip', type=str), self.settings.value('port', type=int))
            self.worker.start.connect(self.worker.run)
            self.worker.start.connect(self.update_console)
            self.worker.finished.connect(self.update_console)
            self.worker.sent.connect(self.update_console)
            self.worker.moveToThread(self.workthread)
            self.worker.start.emit('Task starts!')

app = QtWidgets.QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())
