import subprocess
import threading
import tempfile
import requests
import os.path
import sys
import base64
from socketIO_client import SocketIO, BaseNamespace

RSCR_PATH = 'Rscript'
SERVER = '145.97.202.35'
PORT = 80

class roctoClass(BaseNamespace):
    def on_result_returned(self, returns):
        print('Task arrives.')
        global task_list # Probably a very bad idea...
        task_list = []
        task_list.append(returns)

class Task(object):
    def __init__(self, ip, port):
        self._get_task(ip, port)

    def _get_task(self, ip, port):
        sio = SocketIO(ip, port, roctoClass)
        sio.emit('request_job')
        sio.wait(2)
        sio.disconnect()

        print(task_list)
        results = task_list[0]

        self.id = results['ID']
        self.script_path = results['RSCRIPT']
        self.input_path = results['INPUT']
        self.tmp_dir = tempfile.TemporaryDirectory() # Any reason not to change this into .TemporaryFile?
        self.output = os.path.join(self.tmp_dir.name, 'tmp_output')
        self.tmp_script = os.path.join(self.tmp_dir.name, 'tmp_script')
        self.tmp_input = os.path.join(self.tmp_dir.name, 'tmp_data')

        with open(self.tmp_script, 'wb') as outf:
            remote_iter = requests.get(self.script_path).iter_content(chunk_size=1024)
            [outf.write(i) for i in remote_iter]
        with open(self.tmp_input, 'wb') as outf:
            remote_iter = requests.get(self.input_path).iter_content(chunk_size=1024)
            [outf.write(i) for i in remote_iter]

    def run(self):
        self.proc_ret = subprocess.run([RSCR_PATH, self.tmp_script, self.tmp_input,\
        self.output, str(self.id)], stderr = subprocess.PIPE, stdout = subprocess.PIPE)

        try:
            self.proc_ret.check_returncode()
        except subprocess.CalledProcessError as e:
            print(e)

    def send_results(self, ip, port):
        print('sending')
        self.byte_enc = base64.b64encode(open(self.output, 'rb').read())
        sio = SocketIO(ip, port, roctoClass) # TODO: port should be integer?
        sio.emit('send_results', {
        'ID' : str(self.id),
        'content' : str(self.byte_enc)[2:-1] # removes b''
        })
        sio.disconnect()
