from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

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
