import subprocess
import threading
import os.path
import sys
import base64
import json
from zipfile import ZipFile

import requests
import appdirs


from socketIO_client import SocketIO, BaseNamespace

from .errors import ServerErr

RSCR_PATH = 'Rscript'
INTERM_SCR = 'rocto_client/client/interm.R'
APP_DIR = appdirs.user_data_dir('rocto_client')

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
        self.local_dir = os.path.join(APP_DIR, job_id)

        self.tmp_roctopack = '/home/oghn/MEGAsync/Projeler/ROctopus/ROctopus-server/test/roctoJob.rocto'
        # self.tmp_roctopack = os.path.join(self.local_dir, 'tmp_roctopack')
        # with open(self.tmp_roctopack, 'wb') as outf:
        #     remote_iter = requests.get(self.content_url).iter_content(chunk_size=1024)
        #     [outf.write(i) for i in remote_iter]

    def run(self):
        print(os.path.curdir)
        self.proc_ret = subprocess.run([RSCR_PATH, INTERM_SCR,\
        self.tmp_roctopack, self.local_dir, str(self.iter_no)], stderr = subprocess.PIPE, stdout = subprocess.PIPE)

        try:
            self.proc_ret.check_returncode()
        except subprocess.CalledProcessError as e:
            print(e)

class roctoPack(object):
    def __init__(self, path):
        self.grid = json.loads(ZipFile(path).open('roctoJob/grid.json').read().decode())
        self.meta = json.loads(ZipFile(path).open('roctoJob/meta.json').read().decode())
