import logging
import sys
import psutil

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from rocto_client import API_VERSION
from rocto_client.client import client
from rocto_client.client.errors import ServerErr
from rocto_client.Qt.threads import threadWorker, threadNetworker
from rocto_client.Qt.tablemodel import roctoTableModel
from rocto_client.Qt.ui.importer import AboutDialog, SettingsDialog, Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    """Main Qt window with added signals and slots."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.InitUi()
        self.ui.select_rocto.clicked.connect(self._choose_file)
        self.settings = QtCore.QSettings('rocto_client', 'rocto_client')

    def _create_netwthread(self):
        self.netwthread = QtCore.QThread()
        self.netwthread.start()

    def _create_workthread(self):
        self.workthread = QtCore.QThread()
        self.workthread.start()

    @pyqtSlot()
    def _choose_file(self):
        fd_filter = ".Rocto files (*.rocto)"
        path, __ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file', filter = fd_filter)
        self.ui.rocto_pack = client.roctoPack(path)
        self.ui.table_model = roctoTableModel(self.ui.rocto_pack)
        self.ui.tableView.setModel(self.ui.table_model)
        self.ui.tableView.setEnabled(True)
        self.ui.tableView.doubleClicked.connect(self.ui.table_model._handle_doubleclicked)

    @pyqtSlot(int)
    def _handle_conn_status(self, code):
        if code == 1:
            logging.info('Connected to server.')
            self.ui.connect_button.setText('Disconnect')
            self.ui.textEdit.append('Connected to server.')
            self.ui.runBox.setEnabled(True)
            self.ui.start_button.setEnabled(True)
        elif code == 0:
            logging.info('Disconnected from server.')
            self.ui.textEdit.append('Successfully disconnected from server.')
            self.ui.connect_button.setText('Connect')
        elif code == -1:
            logging.info('Connection problem!')
            self.ui.textEdit.append('Problem connecting to server.')

    @pyqtSlot(str, int)
    def _handle_task_received(self, job_id, iter_no):
        logging.info('Task {}.{} is received.'.format(job_id, iter_no))

        self.ui.textEdit.setEnabled(True)
        self.ui.textEdit.append('Task {}.{} is received.'.format(job_id, iter_no))
        self.ui.start_button.setText('Stop worker!')

        self.local_queue = {}

        for i in self.networker.sio.get_namespace().task_queue:
            self.local_queue[i['jobId']] = client.Task(i['jobId'], i['iterNo'], i['contentUrl'], \
            self.settings.value('r_path', type=str))

        # Reinitialize the list in socketIO_client namespace.
        self.networker.sio.get_namespace().task_queue = []

    @pyqtSlot(int, str)
    def _handle_error_received(self, code, message):
        logging.info('Server returned error: {} - {}'.format(code, message))
        self.ui.textEdit.append('Server returned error {}: {}'.format(code, message))


    @pyqtSlot(str, int)
    def _handle_result_sent(self, job_id, iter_no):
        logging.info('Result of Task {}.{} is sent to server.'.format(job_id, iter_no))
        self.ui.textEdit.setEnabled(True)
        self.ui.textEdit.append('Result of Task {}.{} is sent to server.'.format(job_id, iter_no))

        self.local_queue.pop(job_id)


    @pyqtSlot(str, int)
    def _handle_task_starts(self, task_id, iter_no):
        self.ui.textEdit.append('Task {}.{} started.'.format(task_id, iter_no))

    @pyqtSlot(str, int)
    def _handle_task_finishes(self, task_id, iter_no):
        self.ui.textEdit.append('Task {}.{} finished.'.format(task_id, iter_no))
        self.networker.send_results.emit(self.local_queue[task_id])

    def InitUi(self):
        self.setWindowIcon(QtGui.QIcon(':/icons/icon.png'))
        self.ui.actionPreferences.triggered.connect(self.InitPreferences)
        self.ui.actionAbout.triggered.connect(self.InitAbout)
        self.ui.connect_button.clicked.connect(self.connect_to_server)
        # self.ui.get_task_but.clicked.connect(self.get_task)
        # self.ui.run_button.clicked.connect(self.start_worker) #
        self.ui.start_button.clicked.connect(self.iter_worker)
        self.ui.actionQuit.triggered.connect(QtCore.QCoreApplication.instance().quit)
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
                self.networker.disconnect.connect(self.networker.socket_disconnect)
                self.networker.get_task.connect(self.networker.socket_gettask)
                self.networker.conn_status.connect(self._handle_conn_status)
                self.networker.task_received.connect(self._handle_task_received)
                self.networker.error_received.connect(self._handle_error_received)
                self.networker.result_sent.connect(self._handle_result_sent)
                self.networker.send_results.connect(self.networker.socket_sendresults)
                self.networker.moveToThread(self.netwthread)
                self.networker.init_connect.emit()
            except AttributeError:
                self._create_netwthread()
                self.networker = threadNetworker(self.settings.value('server_ip', type = str),\
                self.settings.value('port', type = int))
                self.networker.init_connect.connect(self.networker.socket_initconnect)
                self.networker.disconnect.connect(self.networker.socket_disconnect)
                self.networker.get_task.connect(self.networker.socket_gettask)
                self.networker.conn_status.connect(self._handle_conn_status)
                self.networker.task_received.connect(self._handle_task_received)
                self.networker.error_received.connect(self._handle_error_received)
                self.networker.result_sent.connect(self._handle_result_sent)
                self.networker.send_results.connect(self.networker.socket_sendresults)
                self.networker.moveToThread(self.netwthread)
                self.networker.init_connect.emit()
        elif self.sender().text() == 'Disconnect':
            self.networker.disconnect.emit()


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
            #       an overall task counter is implmented.
            try:
                self.worker = threadWorker(self.local_queue[i])
                self.worker.start.connect(self.worker.worker_run)
                self.worker.task_starts.connect(self._handle_task_starts)
                self.worker.task_finishes.connect(self._handle_task_finishes)
                self.worker.moveToThread(self.workthread)
                self.worker.start.emit()
            except AttributeError:
                self._create_workthread()
                self.worker = threadWorker(self.local_queue[i])
                self.worker.start.connect(self.worker.worker_run)
                self.worker.task_starts.connect(self._handle_task_starts)
                self.worker.task_finishes.connect(self._handle_task_finishes)
                self.worker.moveToThread(self.workthread)
                self.worker.start.emit()
        logging.info('Task started running.')

    def iter_worker(self):
        if self.sender().text() == 'Start worker!':
            self.networker.task_received.connect(self.start_worker)
            self.networker.result_sent.connect(self.get_task)
            self.get_task()

        elif self.sender().text() == 'Stop worker!':
            self.networker.result_sent.disconnect(self.get_task)
            self.ui.start_button.setText('Kill jobs!')

        elif self.sender().text() == 'Kill jobs!':
            print('Implement kill.')
            self.ui.start_button.setText('Start worker!')


logging.basicConfig(filename = 'log.log', level = logging.DEBUG)
app = QtWidgets.QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())
