import logging
import sys
import psutil

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ROctopus_client.client import client
from ROctopus_client.client.errors import ServerErr
from ROctopus_client.Qt.threads import threadWorker, threadNetworker
from ROctopus_client.Qt.ui.importer import AboutDialog, SettingsDialog, Ui_MainWindow

API_VERSION = '0.1.0'

class MainWindow(QtWidgets.QMainWindow):
    """Main Qt window with added signals and slots."""
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

    @pyqtSlot(int)
    def _handle_conn_status(self, code):
        if code == 1:
            logging.info('Successfully connected to server.')
            self.ui.conn_status.setEnabled(True)
            self.ui.conn_status.setText('Connected!')
            self.ui.connect_button.setText('Disconnect')
            self.ui.runBox.setEnabled(True)
        elif code == 0:
            logging.info('Successfully disconnected from server.')
            self.ui.conn_status.setEnabled(False)
            self.ui.conn_status.setText('Disconnected!')
        elif code == -1:
            logging.info('Connection problem!')
            self.ui.conn_status.setEnabled(False)
            self.ui.conn_status.setText('Disconnected!')
            self.ui.textEdit.append('Problem connecting to server.')

    @pyqtSlot(int, str, int)
    def _handle_netw_task_status(self, status, task_id, iter_no):
        logging.info('Task {}.{} is received.'.format(task_id, iter_no))

        self.ui.run_button.setEnabled(True)
        self.ui.textEdit.setEnabled(True)
        self.ui.textEdit.append('Task {}.{} is received.'.format(task_id, iter_no))
        self.local_queue = {}

        for i in self.networker.sio.get_namespace().task_queue:
            task = client.Task(i['jobId'], i['iterNo'], i['contentUrl'])
            self.local_queue[i['jobId']] = task

    @pyqtSlot(int, str, int)
    def _task_status(self, status, task_id, iter_no):
        if status == -1:
            self.ui.textEdit.append('Task {}.{} started.'.format(task_id, iter_no))
        if status == 0:
            self.ui.textEdit.append('Task {}.{} finished.'.format(task_id, iter_no))
            self.networker.send_results.emit(self.local_queue[task_id])

    def InitUi(self):
        self.setWindowIcon(QtGui.QIcon('icons/icon.png')) # Relative to runtime directory?
        self.ui.actionPreferences.triggered.connect(self.InitPreferences)
        self.ui.actionAbout.triggered.connect(self.InitAbout)
        self.ui.connect_button.clicked.connect(self.connect_to_server)
        self.ui.get_task_but.clicked.connect(self.get_task)
        self.ui.run_button.clicked.connect(self.start_worker)
        self.ui.actionQuit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.ui.quit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.show()

    def InitPreferences(self):
        """Initialize PreferencesDialog."""
        self.preferences_dialog = SettingsDialog()
        self.preferences_dialog.ui.avail_ram.setText(str(round(psutil.virtual_memory().total/1024/1024)))
        self.preferences_dialog.ui.avail_core.setText(str(psutil.cpu_count()))

        # Check if the user had set server_ip, port, sys_ram and sys_cores, username and pw:
        if self.settings.contains('username') and self.settings.contains('pw'):
            self.preferences_dialog.ui.input_username.setText(self.settings.value('username', type=str))
            self.preferences_dialog.ui.input_password.setText(self.settings.value('pw', type=str))

        if self.settings.contains('server_ip') and self.settings.contains('server_ip'):
            self.preferences_dialog.ui.ip_entry.setText(self.settings.value('server_ip', type=str))
            self.preferences_dialog.ui.port_entry.setText(self.settings.value('port', type=str))

        if self.settings.contains('r_path') and self.settings.contains('r_vers'):
            self.preferences_dialog.ui.input_rpath.setText(self.settings.value('r_path', type=str))
            self.preferences_dialog.ui.input_rvers.setText(self.settings.value('r_vers', type=str))

        if self.settings.contains('sys_ram') and self.settings.contains('sys_cores'):
            self.preferences_dialog.ui.input_ram.setValue(self.settings.value('sys_ram', type=int))
            self.preferences_dialog.ui.input_cpu.setValue(self.settings.value('sys_cores', type=int))

        # Get the set values once the window closes. Only if the user hits OK.
        if self.preferences_dialog.exec_(): ## Modal window. Use .show() for modeless.
            values = self.preferences_dialog.getValues()
            for (key, value) in values.items():
                self.settings.setValue(key, value)

    def InitAbout(self):
        """Initialize About dialog."""
        self.about_dialog =  AboutDialog()

    def connect_to_server(self):
        if self.sender().text() == 'Connect':
            try:
                self.networker = threadNetworker(self.settings.value('server_ip', type = str),\
                self.settings.value('port', type = int))
                self.networker.init_connect.connect(self.networker.socket_initconnect)
                self.networker.get_task.connect(self.networker.socket_gettask)
                self.networker.conn_status.connect(self._handle_conn_status)
                self.networker.netw_task_status.connect(self._handle_netw_task_status)
                self.networker.send_results.connect(self.networker.socket_sendresults)
                self.networker.moveToThread(self.netwthread)
                self.networker.init_connect.emit()
            except AttributeError:
                self._create_netwthread()
                self.networker = threadNetworker(self.settings.value('server_ip', type = str),\
                self.settings.value('port', type = int))
                self.networker.init_connect.connect(self.networker.socket_initconnect)
                self.networker.get_task.connect(self.networker.socket_gettask)
                self.networker.conn_status.connect(self._handle_conn_status)
                self.networker.netw_task_status.connect(self._handle_netw_task_status)
                self.networker.send_results.connect(self.networker.socket_sendresults)
                self.networker.moveToThread(self.netwthread)
                self.networker.init_connect.emit()
        elif self.sender().text() == 'Disconnect':
            # TODO: Implement disconnect function?
            pass

    def get_task(self):
        self.networker.get_task.emit({
            'cores' : 1, # 1 is fixed per API 0.1.0 reference. In future: self.settings.value('sys_cores', type=int),
            'memory' : self.settings.value('sys_mem', type = int),
            'RVersion' : self.settings.value('r_vers', type = str),
            'user' : self.settings.value('username', type = str),
            'version' : API_VERSION
        })
        logging.info('Task request sent to server.')

    def start_worker(self):
        for i in self.local_queue:
            # TODO: The loop here means all of the tasks will be run.
            #       Should run only the next job in the queue after
            #       an overall task counter is implmented..
            try:
                self.worker = threadWorker(self.local_queue[i])
                self.worker.start.connect(self.worker.worker_run)
                self.worker.task_status.connect(self._task_status)
                self.worker.moveToThread(self.workthread)
                self.worker.start.emit()
            except AttributeError:
                self._create_workthread()
                self.worker = threadWorker(self.local_queue[i])
                self.worker.start.connect(self.worker.worker_run)
                self.worker.task_status.connect(self._task_status)
                self.worker.moveToThread(self.workthread)
                self.worker.start.emit()
        logging.info('Task started running.')

logging.basicConfig(filename = 'log.log', level = logging.DEBUG)
app = QtWidgets.QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())
