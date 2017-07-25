class ServerErr(Exception):
    """Errors by server"""

    err_dict = {
        '-1' : 'Generic error.',
        '1' : 'No jobs available.',
        '2' : 'Failed to count available jobs',
        '3' : 'No job found.',
        '4' : 'Job failed to lock.',
        '5' : 'User not found.',
        '6' : 'File save failed.'
    }
    def __init__(self, err):
        self.err = err
        self.message = err_dict[err]
        super().__init__(err)
