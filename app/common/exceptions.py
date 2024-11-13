class ValidationException(Exception):
    def __init__(self, source: str, message: str):
        self.source = source
        self.message = message
