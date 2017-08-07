from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from socketIO_client import SocketIO, exceptions
import base64

from rocto_client import API_VERSION
from rocto_client.client.client import roctoClass, Task
from rocto_client.client.errors import ServerErr

class threadNetworker(QtCore.QObject):
    """socketIO network handler."""
    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port

    """Signals to trigger internal methods of threadNetworker."""
    init_connect = pyqtSignal()
    disconnect = pyqtSignal()
    get_task = pyqtSignal(dict)
    send_results = pyqtSignal(Task)

    """Signals to trigger events in the main Qt thread."""
    conn_status = pyqtSignal(int) # 1 for success, -1 for error.
    task_received = pyqtSignal(str, int) # job_id, iter_no.
    error_received = pyqtSignal(int, str)
    result_sent = pyqtSignal(str, int) # job_id, iter_no.

    @pyqtSlot()
    def socket_initconnect(self):
        """Connects to socketIO server and emits conn_status()."""
        try:
            self.sio = SocketIO(self.ip, self.port, roctoClass, wait_for_connection = False)
            self.conn_status.emit(1)
        except exceptions.ConnectionError:
            self.conn_status.emit(-1)

    @pyqtSlot()
    def socket_disconnect(self):
        self.sio.disconnect()
        self.conn_status.emit(0)

    @pyqtSlot(dict)
    def socket_gettask(self, info):
        """Gets task from the socketIO server."""
        # Change according to api/worker.json.
        try:
            # TODO: logging
            self.sio.emit('request_task', info)
            self.sio.wait(.1)
            # Process self.sio.get_namespace().task_queue[0]['version'] here.
            job_id = self.sio.get_namespace().task_queue[0]['jobId']
            iter_no = self.sio.get_namespace().task_queue[0]['iterNo']
            self.task_received.emit(job_id, iter_no)

        except ServerErr as e:
            # TODO: logging
            self.error_received.emit(e.err, e.message)

    @pyqtSlot(Task)
    def socket_sendresults(self, Task):
        """Sends the passed Task to the server."""
        # TODO:ERROR_CATCH

        self.result_sent.emit(Task.job_id, Task.iter_no)
        if self.sio.connected == True:
            self.sio.emit('send_results', {
            'version' : API_VERSION,
            'jobId' : str(Task.job_id),
            'iterNo' : Task.iter_no,
            'exitStatus' : Task.status,
            'content' : str(Task.output)[2:-1] if Task.proc_ret.returncode == 0 else Task.proc # removes b'' # content may change according to exit status
            })
        else:
            self.sio = SocketIO(self.ip, self.port, roctoClass, wait_for_connection = False)
            self.sio.emit('send_results', {
            'version' : API_VERSION,
            'jobId' : str(Task.job_id),
            'iterNo' : Task.iter_no,
            'exitStatus' : Task.status,
            'content' : str(Task.output)[2:-1] # removes b'' # content may change according to exit status
            })

class threadWorker(QtCore.QObject):
    """worker object to run received tasks locally."""
    def __init__(self, task):
        super().__init__()
        self.task = task

    """Signals to trigger internal methods of threadWorker."""
    start = pyqtSignal()

    """Signals to trigger events in the main Qt thread."""
    task_starts = pyqtSignal(str, int)
    task_finishes = pyqtSignal(str, int)

    @pyqtSlot()
    def worker_run(self):
        self.task_starts.emit(self.task.job_id, self.task.iter_no)
        self.task.run()
        self.task_finishes.emit(self.task.job_id, self.task.iter_no)
