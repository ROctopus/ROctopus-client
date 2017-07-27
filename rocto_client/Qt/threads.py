from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from rocto_client.client.client import roctoClass, Task
from socketIO_client import SocketIO, exceptions
import base64

class threadNetworker(QtCore.QObject):
    """socketIO network handler."""
    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port

    """Signals to trigger internal methods of threadNetworker."""
    init_connect = pyqtSignal()
    get_task = pyqtSignal(dict)
    send_results = pyqtSignal(Task)

    """Signals to trigger events in the main Qt thread."""
    conn_status = pyqtSignal(int) # 1 for success, -1 for error.
    netw_task_status = pyqtSignal(int, str, int) # Status, job_id, iter_no.

    @pyqtSlot()
    def socket_initconnect(self):
        """Connects to socketIO server and emits conn_status()."""
        try:
            self.sio = SocketIO(self.ip, self.port, roctoClass, wait_for_connection = False)
            self.conn_status.emit(1)
        except exceptions.ConnectionError:
            self.conn_status.emit(-1)

    @pyqtSlot(dict)
    def socket_gettask(self, info):
        """Gets task from the socketIO server."""
        # Change according to api/worker.json.
        try:
            self.sio.emit('request_task', info)
            self.sio.wait(.1)
            # Process self.sio.get_namespace().task_queue[0]['version'] here.
            job_id = self.sio.get_namespace().task_queue[0]['jobId']
            iter_no = self.sio.get_namespace().task_queue[0]['iterNo']
            self.netw_task_status.emit(0, job_id, iter_no)
            # TODO:ERROR_CATCH
        except ServerErr as e:
            print(e)
            print(err)

    @pyqtSlot(Task)
    def socket_sendresults(self, Task):
        """Sends the passed Task to the server."""
        # TODO:ERROR_CATCH
        # TODO:Emit the status using netw_task_status()

        if self.sio.connected == True:
            byte_enc = base64.b64encode(open(Task.output, 'rb').read()) # DEPRECATED with worker API v0.1.0.
            self.sio.emit('send_results', {
            'jobId' : str(Task.job_id),
            'iterNo' : str(Task.iter_no),
            # 'exitStatus' : send exit status
            'content' : str(byte_enc)[2:-1] # removes b'' # content may change according to exit status
            })
        else:
            self.sio = SocketIO(self.ip, self.port, roctoClass, wait_for_connection = False)
            byte_enc = base64.b64encode(open(Task.output, 'rb').read()) # DEPRECATED with worker API v0.1.0.
            self.sio.emit('send_results', {
            'jobId' : str(Task.job_id),
            'iterNo' : str(Task.iter_no),
            # 'exitStatus' : send exit status
            'content' : str(byte_enc)[2:-1] # removes b'' # content may change according to exit status
            })

class threadWorker(QtCore.QObject):
    """worker object to run received tasks locally."""
    def __init__(self, task):
        super().__init__()
        self.task = task

    """Signals to trigger internal methods of threadWorker."""
    start = pyqtSignal()

    """Signals to trigger events in the main Qt thread."""
    task_status = pyqtSignal(int, str, int) # -1 when task starts, 0 when finishes.

    @pyqtSlot()
    def worker_run(self):
        self.task_status.emit(-1, self.task.job_id, self.task.iter_no)
        self.task.run()
        self.task_status.emit(0, self.task.job_id, self.task.iter_no)
