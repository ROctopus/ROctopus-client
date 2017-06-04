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
    def on_result_returned(self, returns):
        try:
            self.job_queue.append(returns)
        except AttributeError:
            self.job_queue = []
            self.job_queue.append(returns)
    def on_err(self, err):
        raise ServerErr(err)

class Job(object):
    def __init__(self, job_id, script_path, input_path):
        self.job_id = job_id
        self.script_path = script_path
        self.input_path = input_path
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
        self.output, str(self.job_id)], stderr = subprocess.PIPE, stdout = subprocess.PIPE)

        try:
            self.proc_ret.check_returncode()
        except subprocess.CalledProcessError as e:
            print(e)
