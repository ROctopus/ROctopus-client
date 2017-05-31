from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from ROctopus_client.client.client import roctoClass
from socketIO_client import SocketIO

class threadWorker(QtCore.QObject):
    def __init__(self, task, ip, port):
        super().__init__()
        self.task = task
        self.ip = ip
        self.port = port

    start = pyqtSignal(str)
    finished = pyqtSignal(str)
    sent = pyqtSignal(str)

    @pyqtSlot()
    def run(self):
        self.task.run()
        self.finished.emit('Task ' + str(self.task.id) + ' finished!')
        self.task.send_results(self.ip, self.port)
        self.sent.emit('Task ' + str(self.task.id) + ' sent!')

class threadNetworker(QtCore.QObject):
    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port

    initconnect = pyqtSignal()
    conn_status = pyqtSignal(int)
    get_job = pyqtSignal(int)
    job_recv = pyqtSignal()

    @pyqtSlot()
    def socket_connect(self):
        self.sio = SocketIO(self.ip, self.port, roctoClass)
        if self.sio.connected == True:
            self.conn_status.emit(1)
        else:
            pass # Add exception here? See how to combine ServerErr

    @pyqtSlot(int)
    def socket_getjob(self, count):
        self.sio.emit('request_job')
        self.sio.wait(.1)
        self.job_recv.emit()
