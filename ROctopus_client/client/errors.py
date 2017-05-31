class ServerErr(Exception):
    """Raised when no jobs are available at the server."""
    def __init__(self, message):
        super().__init__(message)
