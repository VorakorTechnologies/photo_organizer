class Common:
    def __init__(self):
        super().__init__()


class Error(Exception):
    """Base error class for custom exceptions."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
