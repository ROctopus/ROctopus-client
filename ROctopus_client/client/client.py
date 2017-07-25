import subprocess
import threading
import tempfile
import requests
import os.path
import sys
import base64
from socketIO_client import SocketIO, BaseNamespace

from .errors import ServerErr

RSCR_PATH = 'Rscript'

class roctoClass(BaseNamespace):
    def on_return_task(self, returns):
        print('RETURNS!')
        try:
            self.task_queue.append(returns)
        except AttributeError:
            self.task_queue = []
            self.task_queue.append(returns)
    def on_err(self, err):
        raise ServerErr(err)

class Task(object):
    def __init__(self, job_id, iter_no, content_url):
        self.job_id = job_id
        self.iter_no = iter_no
        self.content_url = content_url
        self.tmp_dir = tempfile.TemporaryDirectory() # or .TemporaryFile?

        # DEPRECATED with worker API v0.1.0
        self.output = os.path.join(self.tmp_dir.name, 'tmp_output')
        self.tmp_script = os.path.join(self.tmp_dir.name, 'tmp_script')
        self.tmp_input = os.path.join(self.tmp_dir.name, 'tmp_data')

        # DEPRECATED with worker API v0.1.0. Waiting for detailed R package
        # definition.
        # with open(self.tmp_script, 'wb') as outf:
        #     remote_iter = requests.get(self.script_path).iter_content(chunk_size=1024)
        #     [outf.write(i) for i in remote_iter]
        # with open(self.tmp_input, 'wb') as outf:
        #     remote_iter = requests.get(self.input_path).iter_content(chunk_size=1024)
        #     [outf.write(i) for i in remote_iter]

    def run(self):
        # DEPRECATED with worker API v0.1.0. Waiting for detailed R package
        # definition.
        self.proc_ret = subprocess.run([RSCR_PATH, self.tmp_script, self.tmp_input,\
        self.output, str(self.task_id)], stderr = subprocess.PIPE, stdout = subprocess.PIPE)

        try:
            self.proc_ret.check_returncode()
        except subprocess.CalledProcessError as e:
            print(e)
