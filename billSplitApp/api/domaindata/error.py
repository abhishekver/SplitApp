from enum import Enum


class Error:
    def __init__(self):
        self.message = ""
        self.type = ""


class ErrorType(Enum):
    INVALID_INPUT = 1
    UNKNOWN = 2
