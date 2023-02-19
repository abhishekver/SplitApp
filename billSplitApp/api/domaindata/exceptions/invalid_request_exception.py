class InvalidRequestException(Exception):
    """Raised when the input is invalid"""

    def __init__(self, message):
        self.message = message
