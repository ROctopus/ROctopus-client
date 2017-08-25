import subprocess
import threading
import os.path
import sys
import base64
import json
from zipfile import ZipFile, BadZipFile

import requests
import appdirs


from socketIO_client import SocketIO, BaseNamespace

from .errors import ServerErr, NotRoctoFile

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
    '''Task object.

    status attribute can be NULL (added), 'started', 0 (finished without error), 1 (error) or -N (killed by signal N)
    '''
    def __init__(self, job_id, iter_no, content_url, rscript_path):
        self.status = None
        self.job_id = job_id
        self.iter_no = iter_no
        self.content_url = content_url
        self.local_dir = os.path.join(APP_DIR, job_id, str(iter_no))
        os.makedirs(self.local_dir)
        self.rscript_path = rscript_path

        # self.tmp_roctopack = '/home/oghn/MEGAsync/Projeler/ROctopus/ROctopus-server/test/roctoJob.rocto'
        self.tmp_roctopack = os.path.join(self.local_dir, '{}_{}.rocto'.format(self.job_id, self.iter_no))
        with open(self.tmp_roctopack, 'wb') as outf:
            remote_iter = requests.get(self.content_url).iter_content(chunk_size=1024)
            [outf.write(i) for i in remote_iter]

    def run(self):
        print(os.path.curdir)
        self.status = 'started'
        self.proc_ret = subprocess.run([self.rscript_path, INTERM_SCR,\
        self.tmp_roctopack, self.local_dir, str(self.iter_no)], stderr = subprocess.PIPE, stdout = subprocess.PIPE)

        try:
            self.proc_ret.check_returncode()
            self.status = 0
            output_path = os.path.join(self.local_dir, '{}_{}-{}.Rdata'.format(self.job_id, self.iter_no, self.iter_no))
            self.output = base64.b64encode(open(output_path, 'rb').read())
        except subprocess.CalledProcessError as e:
            self.status = self.proc_ret.returncode
            self.output = self.proc_ret.stderr.decode()
            print(e)
            print('--- Subprocess stdout: --- \n')
            print(self.proc_ret.stdout.decode())
            print('--- Subprocess stderr: --- \n')
            print(self.proc_ret.stderr.decode())

class roctoPack(object):
    def __init__(self, path):
        try:
            zipfile = ZipFile(path)
        except BadZipFile:
            raise(NotRoctoFile())

        self.path = path
        self.grid = json.loads(zipfile.open('roctoJob/grid.json').read().decode())
        self.meta = json.loads(zipfile.open('roctoJob/meta.json').read().decode())
