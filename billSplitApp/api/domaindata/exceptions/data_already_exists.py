class DataAlreadyExists(Exception):
    """Raised when the data is duplicate"""
    def __init__(self, message):
        self.message = message
