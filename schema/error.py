# -*- coding: utf-8 -*-

class SchemaError(Exception):
    """Exception for this library.
    
    Arguments:
        message(str): Message string containing error message
        locator (:class:`object`): :class:`~.Locator` object (or any
           object with identical interface )
    """
    def __init__(self, message=None, locator=None):
        line= None
        col= None
        if locator:
            line= locator.line
            col= locator.column
        super().__init__(message, line, col)


    @property
    def message(self):
        return self.args[0]

    @property
    def line(self):
        return self.args[1]

    @property
    def column(self):
        return self.args[2]


    def __str__(self):
        return "{}:{}: {}".format(self.line, self.column, self.message)
    
    