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
INTERM_SCR = 'ROctopus_client/client/interm.R'

class roctoClass(BaseNamespace):
    def on_return_task(self, returns):
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


        self.tmp_roctopack = os.path.join(self.tmp_dir.name, 'tmp_roctopack')
        with open(self.tmp_roctopack, 'wb') as outf:
            remote_iter = requests.get(self.content_url).iter_content(chunk_size=1024)
            [outf.write(i) for i in remote_iter]

    def run(self):
        print(os.path.curdir)
        self.proc_ret = subprocess.run([RSCR_PATH, INTERM_SCR,\
        self.tmp_roctopack, self.tmp_dir.name, str(self.iter_no)], stderr = subprocess.PIPE, stdout = subprocess.PIPE) # WARNING@27/07: self.tmp_dir should change. Where to deliver the files to users?

        try:
            self.proc_ret.check_returncode()
        except subprocess.CalledProcessError as e:
            print(e)
