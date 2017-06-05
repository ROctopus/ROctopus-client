from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from ROctopus_client.client.client import roctoClass, Job
from socketIO_client import SocketIO, exceptions
import base64

class threadWorker(QtCore.QObject):
    # This is not a thread but a worker to put in a thread!
    def __init__(self, task):
        super().__init__()
        self.task = task

    start = pyqtSignal()
    task_status = pyqtSignal(int, int)

    @pyqtSlot()
    def worker_run(self):
        self.task_status.emit(-1, self.task.task_id)
        self.task.run()
        self.task_status.emit(0, self.task.task_id)

class threadNetworker(QtCore.QObject):
    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port

    initconnect = pyqtSignal()
    conn_status = pyqtSignal(int)
    get_job = pyqtSignal(int)
    send_results = pyqtSignal(Job)
    netw_job_status = pyqtSignal(int, int)

    @pyqtSlot()
    def socket_connect(self):
        try:
            self.sio = SocketIO(self.ip, self.port, roctoClass, wait_for_connection = False)
            self.conn_status.emit(1)
        except exceptions.ConnectionError:
            self.conn_status.emit(-1)

    @pyqtSlot(int)
    def socket_getjob(self, count):
        self.sio.emit('request_job')
        self.sio.wait(.1)
        task_id = self.sio.get_namespace().job_queue[-1]['ID']
        self.netw_job_status.emit(-1, task_id)

    @pyqtSlot(Job)
    def socket_send_results(self, job):
        # Switch this to try except. Need to look into raising an error
        # in case of no connection.
        if self.sio.connected == True:
            byte_enc = base64.b64encode(open(task.output, 'rb').read())
            self.sio.emit('send_results', {
            'ID' : str(job.job_id),
            'content' : str(byte_enc)[2:-1] # removes b''
            })
        else:
            self.sio = SocketIO(self.ip, self.port, roctoClass, wait_for_connection = False)
            byte_enc = base64.b64encode(open(task.output, 'rb').read())
            self.sio.emit('send_results', {
            'ID' : str(task.task_id),
            'content' : str(byte_enc)[2:-1] # removes b''
            })
