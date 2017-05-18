import subprocess
import threading
import tempfile
import requests
import os.path
import sys
import base64
from socketIO_client import SocketIO, BaseNamespace

RSCR_PATH = 'Rscript'
SERVER = None # Change with server IP and port, until GUI arrives.
PORT = None

class Task():
    task_id = None
    script_path = None
    data_path = None

    def __init__(self, task_id, script_path, data_path):
        self.id = task_id
        self.script_path = script_path
        self.data_path = data_path
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.output = os.path.join(self.tmp_dir.name, 'tmp_output')
        self.tmp_script = os.path.join(self.tmp_dir.name, 'tmp_script')
        self.tmp_data = os.path.join(self.tmp_dir.name, 'tmp_data')


        with open(self.tmp_script, 'wb') as outf:
            remote_iter = requests.get(self.script_path).iter_content(chunk_size=1024)
            [outf.write(i) for i in remote_iter]
        with open(self.tmp_data, 'wb') as outf:
            remote_iter = requests.get(self.data_path).iter_content(chunk_size=1024)
            [outf.write(i) for i in remote_iter]

    def run(self):
        self.proc_ret = subprocess.run([RSCR_PATH, self.tmp_script, self.tmp_data,\
        self.output, str(self.id)], stderr = subprocess.PIPE, stdout = subprocess.PIPE)

        try:
            self.proc_ret.check_returncode()
        except subprocess.CalledProcessError as e:
            print(e)


class roctoClass(BaseNamespace):
    def on_result_returned(self, results):
        # Requires task_list=[], not cool.
        task_list.append(Task(results['ID'], results['RSCRIPT'], results['INPUT']))

if __name__ == '__main__':

    # To be replaced with GUI loop.
    task_list = []
    sio = SocketIO(SERVER, PORT, roctoClass)
    sio.emit('request_job')
    sio.wait(2)

    [i.run() for i in task_list]

    for i in task_list:
        if i.proc_ret.returncode == 0:
            byte_enc = base64.b64encode(open(i.output, 'rb').read())
            print('Finished task going back!')
            sio.emit('send_results', {
            'filename' : str(i.id) + i.output,
            'content' : str(byte_enc)
            })
