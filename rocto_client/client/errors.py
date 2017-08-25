class NotRoctoFile(Exception):
    """Raised if the user selects a file which is not a zip file."""

    def __init__(self):
        self.msg = 'The file you chose was not a valid .rocto file.'
        super().__init__(self.msg)

class NoConnection(Exception):
    """Errors by client."""

    def __init__(self):
        self.msg = 'The client is not connected to server.'
        super().__init__(self.msg)

class ServerErr(Exception):
    """Errors by server"""

    err_dict = {
        -1 : 'Generic error.',
        1 : 'No jobs available.',
        2 : 'Failed to count available jobs',
        3 : 'No job found.',
        4 : 'Job failed to lock.',
        5 : 'User not found.',
        6 : 'File save failed.'
    }
    def __init__(self, err):
        self.err = err
        self.message = self.err_dict[err]
        super().__init__(err)
